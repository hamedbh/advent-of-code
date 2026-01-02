use std::path::PathBuf;

pub struct Paths {
    pub project_root: PathBuf,
    pub inputs_dir: PathBuf,
    pub examples_dir: PathBuf,
    pub outputs_dir: PathBuf,
    pub rust_outputs_dir: PathBuf,
    pub example_outputs_dir: PathBuf,
    pub timings_file: PathBuf,
}
impl Paths {
    pub fn new() -> Self {
        let project_root = find_project_root();
        let data_dir = project_root.join("data");
        Self {
            project_root: project_root.clone(),
            inputs_dir: data_dir.join("inputs"),
            examples_dir: data_dir.join("examples"),
            outputs_dir: data_dir.join("outputs"),
            rust_outputs_dir: data_dir.join("outputs").join("rust"),
            example_outputs_dir: data_dir.join("example_outputs"),
            timings_file: data_dir.join("timings").join("timings.csv"),
        }
    }
}
fn find_project_root() -> PathBuf {
    let mut current = std::env::current_dir().unwrap();
    loop {
        if current.join(".venv").exists() {
            return current;
        }
        if !current.pop() {
            panic!("Could not find project root");
        }
    }
}
