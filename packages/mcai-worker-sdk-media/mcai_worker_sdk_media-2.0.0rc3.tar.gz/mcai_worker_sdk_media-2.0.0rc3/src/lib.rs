use pyo3::prelude::*;

mod callback;
mod description;
mod helper;
mod instance;
mod logger;
mod parameters;
mod worker;

#[cfg(feature = "media")]
mod media;

pub const WORKER_METHOD_INIT: &str = "setup";

#[cfg(not(feature = "media"))]
pub const WORKER_METHOD_PROCESS: &str = "process";

#[pymodule]
#[pyo3(name = "mcai_worker_sdk")]
fn py_mcai_worker_sdk(py: Python, m: &PyModule) -> PyResult<()> {
  m.add_class::<worker::Worker>()?;
  m.add_class::<parameters::WorkerParameters>()?;

  #[cfg(feature = "media")]
  {
    m.add_class::<media::AudioStreamDescriptor>()?;
    m.add_class::<media::DataStreamDescriptor>()?;
    m.add_class::<media::VideoStreamDescriptor>()?;

    m.add_class::<media::PyGenericFilter>()?;
  }

  logger::setup_logging(py)?;

  Ok(())
}
