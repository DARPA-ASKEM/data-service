from typing import Callable, Any

def create_pipeline(*funcs: Callable) -> Callable:
    def stateful_compose(original: Any) -> Any:
        val = original
        for func in funcs:
            val = func(val)
        return val
    return stateful_compose

# omymodels can't ;( handle trailing commas
patch_trailing_commas = lambda text: text.replace(',\n)', '\n)')
patch_nomenclature = lambda text: text.replace('blob', 'varchar')
patch_uppercase = lambda text: text.replace('NULL', 'null')
patch = create_pipeline(patch_trailing_commas, patch_nomenclature, patch_uppercase)
