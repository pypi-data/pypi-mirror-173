use crate::instance::WorkerInstance;
#[cfg(feature = "media")]
use crate::media;

use mcai_worker_sdk::prelude::*;
use pyo3::{exceptions::PyNotImplementedError, prelude::*, types::PyType};

#[pyclass(subclass)]
#[derive(Clone, Debug)]
pub struct Worker {
  parameters: Option<Py<PyType>>, // This won't be exposed in Python
}

/// Worker base class to extend
#[pymethods]
impl Worker {
  #[new]
  fn new() -> Worker {
    Worker { parameters: None }
  }

  fn __init__(&mut self, parameters: &PyType, py: Python<'_>) -> PyResult<()> {
    self.parameters = Some(parameters.into_py(py));
    Ok(())
  }

  /// Method called once to set up the worker.
  /// It may be used to load specific resources, perform checks, etc. before processing jobs.
  /// This method is optional.
  fn setup(_: Py<PyAny>) -> PyResult<()> {
    Ok(())
  }

  /// Method called for processing the job.
  /// This method must be re-implemented in the worker.
  #[cfg(not(feature = "media"))]
  fn process(_: Py<PyAny>) -> PyResult<()> {
    Err(PyNotImplementedError::new_err(
      "Init process method must be implemented",
    ))
  }

  /// Method called for initializing the media process.
  /// It must return a list of stream descriptors that will be handled during process
  /// This method must be re-implemented in the worker.
  #[cfg(feature = "media")]
  fn init_process(
    _: Py<PyAny>,
    _format_context: Py<PyAny>,
    _parameters: Py<PyAny>,
  ) -> PyResult<Vec<media::GenericStreamDescriptor>> {
    Err(PyNotImplementedError::new_err(
      "Init process method must be implemented",
    ))
  }

  /// Method called for processing frames.
  /// This method must be re-implemented in the worker.
  #[cfg(feature = "media")]
  fn process_frames(
    _: Py<PyAny>,
    _job_id: Py<PyAny>,
    _stream_index: Py<PyAny>,
    _frames: Py<PyAny>,
  ) -> PyResult<PyObject> {
    Err(PyNotImplementedError::new_err(
      "Init process method must be implemented",
    ))
  }

  /// Method called for processing frames.
  /// This method is optional.
  #[cfg(feature = "media")]
  fn ending_process(_: Py<PyAny>) -> PyResult<()> {
    Ok(())
  }

  /// Method called for starting the worker.
  /// This method must not be re-implemented.
  fn start(self_: PyRef<Self>, py: Python<'_>) {
    let params = self_.parameters.as_ref().unwrap().clone();
    let worker = self_.into_py(py);

    py.allow_threads(|| {
      let wrapper = WorkerInstance::new(worker, params);
      start_worker(wrapper);
    });
  }
}
