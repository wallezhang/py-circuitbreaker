# py-circuitbreaker
A circuit breaker for python

## Usage

1. Initialize a sliding window

    ```python
    from circuitbreaker.circuitbreaker import initialize_circuit_breaker
    
    RATE = 1000
    PERIOD = 10 * 1000
    VOLUME_THRESHOLD = 10
    SLEEP_WINDOW_IN_MILLISECONDS = 2000
    
    window = initialize_circuit_breaker(RATE, PERIOD, VOLUME_THRESHOLD, SLEEP_WINDOW_IN_MILLISECONDS)
    ```

2. Custom two functions

    A function that judge whether the real function result is fail. `res` is real function's return value.

    ```python
    def judge_fail_fn(res):
        return res is None
    ```

    Another function is callback when breaker's status is OPEN. The parameters are passed in real function.

    ```python
    def fallback_fn(*args, **kwargs):
        return 'fallback'
    ```

3. Apply the breaker

    Add a decorator to the function.

    ```python
    from circuitbreaker.circuitbreaker import circuit_breaker

    @circuit_breaker(window, judge_fail_fn, fallback_fn)
    def handler(*args):
        return args[0]
    ```
