#### Diagram
![architect](https://github.com/mercari/ml-system-design-pattern/blob/master/Operation-patterns/Model-load-pattern/diagram.png?raw=true)
### 

- Usecase:
    - When update cycle of a model is more frequent than server image update.
    - When you want to reuse a server image for serving multiple models.

- Pros: 
    - Separate model versioning and image versioning.
    - Reuse of server image.
    - Light image size.
    - Change management of server image becomes easier.
- Cons:
    - It may take longer to start the service. The server although up should be treated as unhealthy until the model load completes.
    - A new requirement of matching supported library versions between images and models is applicable for this pattern.


