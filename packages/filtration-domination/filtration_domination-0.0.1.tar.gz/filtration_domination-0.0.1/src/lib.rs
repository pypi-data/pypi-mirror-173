use ::filtration_domination::edges::{BareEdge, EdgeList, FilteredEdge};
use ::filtration_domination::OneCriticalGrade;
use ::filtration_domination::removal::EdgeOrder;
use ordered_float::OrderedFloat;
use pyo3::prelude::*;

type BifilteredEdge = ((usize, usize), (f64, f64));

fn vector_to_edge_list(edges: Vec<BifilteredEdge>) -> EdgeList<FilteredEdge<OneCriticalGrade<OrderedFloat<f64>, 2>>> {
    let mut edge_list = EdgeList::new(0);
    for ((u, v), (g1, g2)) in edges {
        edge_list.add_edge(FilteredEdge {
            grade: OneCriticalGrade([OrderedFloat(g1), OrderedFloat(g2)]),
            edge: BareEdge(u, v),
        });
    }
    edge_list
}

fn edge_list_to_vector(edge_list: &EdgeList<FilteredEdge<OneCriticalGrade<OrderedFloat<f64>, 2>>>) -> Vec<BifilteredEdge> {
    let mut edges = Vec::with_capacity(edge_list.edges().len());
    for e in edge_list.edge_iter() {
        let bare_edge = (e.edge.0, e.edge.1);
        let grade = (e.grade.0[0].0, e.grade.0[1].0);
        edges.push((bare_edge, grade))
    }
    edges
}

#[pyfunction]
fn remove_strongly_filtration_dominated(edges: Vec<BifilteredEdge>) -> PyResult<Vec<BifilteredEdge>> {
    let mut edge_list = vector_to_edge_list(edges);
    let reduced = ::filtration_domination::removal::remove_strongly_filtration_dominated(&mut edge_list, EdgeOrder::ReverseLexicographic);
    Ok(edge_list_to_vector(&reduced))
}

/// A Python module implemented in Rust.
#[pymodule]
fn filtration_domination(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(remove_strongly_filtration_dominated, m)?)?;
    Ok(())
}