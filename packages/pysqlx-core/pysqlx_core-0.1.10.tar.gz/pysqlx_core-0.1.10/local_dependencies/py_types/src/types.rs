use chrono::SecondsFormat;
use pyo3::types::PyBytes;
use pyo3::{PyObject, Python, ToPyObject};
use quaint::Value;
use serde::Deserialize;

// this type is a placeholder for the actual type
type PyValueList = Vec<PyValue>;

#[derive(Debug, Clone, PartialEq, PartialOrd, Deserialize)]
#[serde(untagged)]
pub enum PyValue {
    // true, false
    Boolean(bool),
    // text
    String(String),
    // red, green, blue
    Enum(String),
    // 1.0
    Int(i64),
    // Vec<String>,
    List(PyValueList),
    // { "name": "foo", "age": 42 }
    Json(String),
    // <body>...</body>
    Xml(String),
    // 00000000-0000-0000-0000-000000000000
    Uuid(String),
    // 00:00:00
    Time(String),
    // 2020-01-01
    Date(String),
    // 2020-01-01T00:00:01
    DateTime(String),
    // 18373737.8274
    Float(f64),
    // Vec<u8>
    Bytes(Vec<u8>),
    // None
    Null,
}

impl<'a> From<Value<'a>> for PyValue {
    fn from(value: Value) -> Self {
        match value {
            Value::Boolean(Some(b)) => PyValue::Boolean(b),
            Value::Enum(s) => s
                .map(|s| PyValue::Enum(s.into_owned()))
                .unwrap_or(PyValue::Null),
            Value::Int32(Some(i)) => PyValue::Int(i as i64),
            Value::Int64(Some(i)) => PyValue::Int(i),
            Value::Array(Some(l)) => {
                let mut list = Vec::new();
                for item in l {
                    list.push(PyValue::from(item));
                }
                PyValue::List(list)
            }
            Value::Json(Some(s)) => PyValue::Json(s.to_string()),
            Value::Xml(Some(s)) => PyValue::Xml(s.to_string()),
            Value::Uuid(Some(s)) => PyValue::Uuid(s.to_string()),
            Value::Time(Some(s)) => PyValue::Time(s.to_string()),
            Value::Date(Some(s)) => PyValue::Date(s.to_string()),
            Value::DateTime(Some(s)) => {
                PyValue::DateTime(s.to_rfc3339_opts(SecondsFormat::Millis, true))
            }
            Value::Float(Some(s)) => PyValue::Float(s as f64),
            Value::Double(Some(s)) => PyValue::Float(s),
            Value::Bytes(Some(b)) => PyValue::Bytes(b.into_owned()),
            Value::Text(Some(s)) => PyValue::String(s.to_string()),
            Value::Char(Some(s)) => PyValue::String(s.to_string()),
            Value::Numeric(Some(s)) => PyValue::String(s.to_string()),
            _ => PyValue::Null,
        }
    }
}

impl<'a> ToPyObject for PyValue {
    fn to_object(&self, py: Python) -> PyObject {
        match self {
            PyValue::Boolean(b) => b.to_object(py),
            PyValue::String(s) => s.to_object(py),
            PyValue::Enum(s) => s.to_object(py),
            PyValue::Int(i) => i.to_object(py),
            PyValue::List(l) => {
                let mut list = Vec::new();
                for item in l {
                    list.push(item.to_object(py));
                }
                list.to_object(py)
            }
            PyValue::Json(s) => s.to_object(py),
            PyValue::Xml(s) => s.to_object(py),
            PyValue::Uuid(s) => s.to_object(py),
            PyValue::Time(s) => s.to_object(py),
            PyValue::Date(s) => s.to_object(py),
            PyValue::DateTime(s) => s.to_object(py),
            PyValue::Float(f) => f.to_object(py),
            PyValue::Bytes(b) => PyBytes::new(py, b).to_object(py),
            PyValue::Null => py.None(),
        }
    }
}
