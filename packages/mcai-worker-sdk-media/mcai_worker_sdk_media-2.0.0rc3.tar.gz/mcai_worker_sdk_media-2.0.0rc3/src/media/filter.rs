use mcai_worker_sdk::prelude::GenericFilter;
use pyo3::{
  prelude::*,
  types::{PyDict, PyList},
};
use std::collections::HashMap;

/// Filter class to define ffmpeg filter that will be applied to the media stream
#[pyclass]
#[derive(Clone, Debug)]
#[pyo3(name = "Filter")]
pub struct PyGenericFilter {
  #[pyo3(get)]
  pub name: String,
  #[pyo3(get)]
  pub label: Option<String>,
  #[pyo3(get)]
  pub parameters: HashMap<String, String>,
}

#[pymethods]
impl PyGenericFilter {
  /// Instantiate a new filter with a given name and label (optional)
  #[new]
  pub fn new(name: String, label: Option<String>) -> PyGenericFilter {
    PyGenericFilter {
      name,
      label,
      parameters: HashMap::default(),
    }
  }

  /// Method to add parameters to a filter
  ///
  /// # Examples
  ///
  /// ```python
  /// import mcai_worker_sdk as mcai
  /// crop_filter = mcai.Filter(name="crop", label="crop_filter")
  /// crop_filter.add_parameters(out_w=10, out_h=20)
  /// ```
  #[args(py_kwargs = "**")]
  fn add_parameters(&mut self, py_kwargs: Option<&PyDict>) {
    if let Some(kwargs) = py_kwargs {
      kwargs.iter().for_each(|(k, v)| {
        self.parameters.insert(k.to_string(), v.to_string());
      })
    }
  }
}

impl From<&PyGenericFilter> for GenericFilter {
  fn from(filter: &PyGenericFilter) -> Self {
    GenericFilter {
      name: filter.name.clone(),
      label: filter.label.clone(),
      parameters: filter.parameters.clone(),
    }
  }
}

pub(crate) fn extract_generic_filters(py_list: &PyList) -> PyResult<Vec<GenericFilter>> {
  Ok(
    py_list
      .iter()
      .map(|item| item.extract::<PyGenericFilter>())
      .collect::<PyResult<Vec<PyGenericFilter>>>()?
      .iter()
      .map(GenericFilter::from)
      .collect(),
  )
}

#[test]
pub fn test_py_filter_creation_with_name() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let filter = PyCell::new(
      py,
      PyGenericFilter {
        name: "my_filter".to_string(),
        label: None,
        parameters: Default::default(),
      },
    )
    .unwrap();

    assert_eq!(filter.borrow().name, "my_filter");
    assert_eq!(filter.borrow().label, None);
    assert_eq!(filter.borrow().parameters, HashMap::new());
  });
}

#[test]
pub fn test_py_filter_creation_with_label() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let filter = PyCell::new(
      py,
      PyGenericFilter {
        name: "my_filter".to_string(),
        label: Some("my_label".to_string()),
        parameters: Default::default(),
      },
    )
    .unwrap();

    assert_eq!(filter.borrow().name, "my_filter");
    assert_eq!(filter.borrow().label, Some("my_label".to_string()));
    assert_eq!(filter.borrow().parameters, HashMap::new());
  });
}

#[test]
pub fn test_py_filter_creation_with_parameters() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let filter = PyCell::new(
      py,
      PyGenericFilter {
        name: "my_filter".to_string(),
        label: None,
        parameters: Default::default(),
      },
    )
    .unwrap();

    let kwargs = PyDict::new(py);
    kwargs.set_item("width", 100).unwrap();
    kwargs.set_item("height", 200).unwrap();
    filter
      .call_method("add_parameters", (), Some(kwargs))
      .unwrap();

    assert_eq!(
      filter.borrow().parameters,
      HashMap::from([
        ("width".to_string(), "100".to_string()),
        ("height".to_string(), "200".to_string())
      ])
    )
  });
}
