use mcai_worker_sdk::prelude::*;
use pyo3::prelude::*;
use std::sync::{Arc, Mutex};

#[pyclass]
pub struct CallbackHandle {
  pub channel: Option<McaiChannel>,
  pub job_id: u64,
  pub job_status: Arc<Mutex<Option<JobStatus>>>,
}

#[pymethods]
impl CallbackHandle {
  fn publish_job_progression(&self, value: u8) -> bool {
    publish_job_progression(self.channel.clone(), self.job_id, value).is_ok()
  }

  fn is_stopped(&self) -> bool {
    if let Some(channel) = &self.channel {
      channel.lock().unwrap().is_stopped()
    } else {
      false
    }
  }

  fn set_job_status(&mut self, status: &str) -> bool {
    let mut job_status = self.job_status.lock().unwrap();
    *job_status = match status {
      "completed" => Some(JobStatus::Completed),
      "processing" => Some(JobStatus::Processing),
      "stopped" => Some(JobStatus::Stopped),
      "error" => Some(JobStatus::Error),
      _ => None,
    };
    job_status.is_some()
  }
}
