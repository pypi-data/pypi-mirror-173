#[macro_export]
macro_rules! setup_wrap {
    ($struct_name:ident, $enum_name:ty, $from_py:ty) => {
        /// NOTE: it's *not* valid to cache by bytes. The hash maybe depends on object
        /// pointer equality, so if you let a given item be deallocated, you can get
        /// collisions!
        #[pyclass]
        #[derive(Clone)]
        pub struct $struct_name {
            data: $enum_name,
            hash: HashBytes,
        }

        impl Debug for $struct_name {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                self.data.fmt(f)
            }
        }

        impl $crate::eq_by_big_hash::EqByBigHash for $struct_name {
            fn hash(&self) -> HashBytes {
                self.hash
            }
        }
        $crate::impl_both_by_big_hash!($struct_name);

        impl $struct_name {
            pub fn data(&self) -> &$enum_name {
                &self.data
            }

            pub fn new(data: $enum_name) -> Self {
                let mut hasher = blake3::Hasher::new();
                hasher.update(&data.uuid());
                data.item_hash(&mut hasher);

                Self {
                    data,
                    hash: hasher.finalize().into(),
                }
            }
        }

        impl From<$enum_name> for $struct_name {
            fn from(x: $enum_name) -> Self {
                Self::new(x)
            }
        }

        impl $enum_name {
            paste::paste! {
                pub fn [<to_ $struct_name:snake>](self) -> $struct_name {
                    self.into()
                }
            }
        }

        impl $from_py {
            paste::paste! {
                pub fn [<to_ $struct_name:snake>](self) -> $struct_name {
                    self.into()
                }
            }
        }

        #[pymethods]
        impl $struct_name {
            fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
                use_rust_comp(&self, &object, comp_op)
            }
            fn __hash__(&self) -> u64 {
                self.first_u64()
            }
            fn debug_print_to_str(&self) -> String {
                format!("{:?}", self)
            }
        }
    };
}

#[macro_export]
macro_rules! setup_callable {
    ($struct_name:ident, $enum_name:ty, $from_py:ty, $func_name:ident ($($arg_name:ident : $arg_ty:ty),*) -> $func_ret:ty) => {
        $crate::setup_wrap!($struct_name, $enum_name, $from_py);

        paste::paste!{
            #[derive(Clone)]
            pub struct [<Raw $struct_name>](Arc<dyn Fn($($arg_ty,)*) -> PyResult<$func_ret> + Send + Sync>);

            impl Debug for [<Raw $struct_name>] {
                fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                    f.debug_tuple(&("Raw".to_owned() + stringify!($struct_name))).finish()
                }
            }
        }

        #[pymethods]
        impl $struct_name {
            fn __call__(&self, _py: Python<'_>, $($arg_name : $arg_ty,)*) -> PyResult<$func_ret> {
                self.$func_name($($arg_name,)*)
            }
        }

        impl $struct_name {
            pub fn new_func<F: Fn($($arg_ty,)*) -> $func_ret + Send + Sync + 'static>(func: F) -> Self {
                Self::new_func_err(move |n| Ok(func(n)))
            }

            pub fn new_func_err<F: Fn($($arg_ty,)*) -> PyResult<$func_ret> + Send + Sync + 'static>(
                func: F,
            ) -> Self {
                Self::new_func_err_arc(Arc::new(func))
            }

            pub fn new_func_err_arc(func: Arc<dyn Fn($($arg_ty,)*) -> PyResult<$func_ret> + Send + Sync>) -> Self {
                paste::paste! {
                    $enum_name::Raw([<Raw $struct_name>](func)).into()
                }
            }
        }

    };
}
