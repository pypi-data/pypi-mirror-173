#![allow(unstable_name_collisions, unused_mut)]

use hashbrown::HashMap;
use pyo3::prelude::*;
use rayon::prelude::*;

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

    lines.iter().cloned().for_each(|(name, seq)| {
        let key = (seq.len(), seq[0..10].to_string());
        let tuplet = (name, seq);

        clusters.entry(key).or_insert(Vec::new()).push(tuplet);
    });

    clusters
        .par_iter()
        .map(|(_, cluster)| {
            let pairs = cluster
                .iter()
                .cloned()
                .map(|x| (x, cluster.clone()))
                .collect::<Vec<_>>();

            let this_lead = pairs
                .par_iter()
                .map(|((_, lead_seq), v)| {
                    let this_this_lead = v
                        .par_iter()
                        .map(|(header, seq_candidate)| {
                            match seqs_within_distance(seq_candidate.clone(), lead_seq.clone(), 1) {
                                true => Some(vec![header.clone(), seq_candidate.clone()]),
                                false => None,
                            }
                        })
                        .filter(|x| x.is_some())
                        .map(|x| x.unwrap())
                        .flatten()
                        .collect::<Vec<_>>();
                    this_this_lead
                })
                .flatten()
                .collect();

            this_lead
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
        .map(|(s1, s2)| match s1 == s2 {
            true => 1,
            false => 0,
        })
        .sum::<u32>();
    final_distace <= max_distance
}

#[pymodule]
fn blosumak(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(cluster_distance_filter, m)?)?;
    Ok(())
}
