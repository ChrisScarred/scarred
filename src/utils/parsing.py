from typing import Any, Dict


def nested_getter(dct: Dict, var: str, def_val: Any = None) -> Any:
        """Obtain a value of a variable in a nested dict.
        
        Args:
            var (str): The variable to obtain.
            def_val (Any, optional): The default value to use if the variable is not set. Defaults to None.
        Returns:
            Any: The value of the queried variable or the default value if the variable is unset and the default is supplied.
        """
        keys = var.split(".")
        n = len(keys)

        if n == 1:
            return dct.get(var, def_val)
        
        val = dct
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k, {})
            else:
                return def_val
        
        return val
