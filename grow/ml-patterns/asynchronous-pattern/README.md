#### Diagram
![architect](https://github.com/mercari/ml-system-design-pattern/blob/master/Serving-patterns/Asynchronous-pattern/diagram1.png?raw=true)
### 

- Usecase:
    - When the immediate process does not depend on the prediction.
    - When you want to reuse a server image for serving multiple models.

- Pros: 
    - You can separate client and prediction.
    - The client does not have to wait for the prediction latency.
- Cons:
    - Requires queue, cache or similar kind of proxy.
    - Not fit to real-time usecase.
