#![allow(unstable_name_collisions, unused_mut)]

use hashbrown::HashMap;
use itertools::Itertools;
use pyo3::prelude::*;
use rayon::prelude::*;
use std::thread;
use crossbeam_channel::unbounded;

/*
Notes to Igster and Kevin:

I tried my best to use parallelism within the outer iterator. But within the inner
iterator I still can't find a pattern to make it parallel. That's because par_iter()
does uses FnOne() that does not accept mutable variables.

 I removed other functions in this branch for clarity. Feel free to rename the functions 
 and merge it with master.

 Also I changed &str to String because PyO3 can't accept references to the stack easily.
 However if you feel like &str is faster please feel free to convert them back. Mind you that
 par_iter() may cause lifetime troubles again for the use of FnOnce() in it. I'm not sure why that happens.

 What I did besides that was heavy use of iterators. That's basically it.

 Please test it and let me know if it's faster or slower. I would do it myself but I'm very tired right now.

 Since Igster is sick I will test it when I wake up later today/tonight.

 Thanks.

 *** IMPORTANT ***: The helper functions do not need to have pyfunction macro.
                    They don't need to be added to the module as well..

*/


#[pyfunction]
fn cluster_distance_filter(lines: Vec<(String, String)>) -> Vec<Vec<String>> {
    let mut clusters = HashMap::new();

    lines
        .iter()
        .cloned()       
        .for_each(|(name, seq)| {
            let key = (seq.len(), seq[0..10].to_string());
            let tuplet = (name, seq);

            clusters.entry(key).or_insert(Vec::new()).push(tuplet);
        });

    

    clusters
        .par_iter()
        .map(|(_, cluster)| {
            let (sender, receiver) = unbounded();
            let mut size = 0usize;
            let mut threads_to_join = vec![];

            cluster
                .iter()
                .cloned()
                .batching(|mut it| match it.next() {
                    None => None,
                    Some(x) => Some(it.clone().intersperse(x)),
                })
                .for_each(|it| {
                    it.batching(|mut iti| match iti.next() {
                        None => None,
                        Some(x) => match iti.next() {
                            None => None,
                            Some(y) => Some((x, y)),
                        },
                    })
                    .for_each(|((header, candidate), (_, lead))| {
                        let ctx = sender.clone();
                        size += 1;

                        let thread_to_join = thread::spawn(move || {
                            match seqs_within_distance(candidate.clone(), lead, 1) {
                                true => {
                                    ctx.send(vec![
                                        header,
                                        candidate,
                                    ]).unwrap();
                                }
                                false => ctx.send(vec![String::new(), String::new()]).unwrap(),
                            }
                        });

                        threads_to_join.push(thread_to_join);
                    });
                });

        let mut this_lead = Vec::with_capacity(size);

        (0..size)
            .into_iter()
            .for_each(|_| this_lead.push(receiver.recv()));

        for thr in threads_to_join {
            thr.join().expect("Thread errored out");
            }
        
        this_lead.iter().cloned().map(|v| v.expect("Error with receiver")).flatten().collect_vec()
    })
    .collect()


}

fn seqs_within_distance(first: String, second: String, max_distance: u32) -> bool {
    let (array_one, array_two) = (first.as_bytes(), second.as_bytes());
    if array_one.len() != array_two.len() {
        return false;
    }

    let final_distace = array_one
                                    .par_iter()
                                    .zip(array_two.par_iter())
                                    .map(|(s1, s2)| {
                                        match s1 == s2 {
                                            true => 1,
                                            false => 0,
                                        }
                                    })
                                    .sum::<u32>();
    final_distace <= max_distance
}

#[pymodule]
fn blosumak(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(cluster_distance_filter, m)?)?;
    Ok(())
}
