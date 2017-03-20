# cs7637-LabInformer

This project implements a chatbot using API.AI, designed to inform the user about Research Labs and associated faculty under the School of Interactive Computing, GeorgiaTech.

  
To converse with the chatbot, please go to the link:
[LabsInformer](https://bot.api.ai/6fe9d3a8-ea54-446a-9e77-76813c8c521b)

*The project is deployed on heroku, and may sometimes fail to respond during conversation and throw the following error:  
```
Webhook call failed. Error: Request timeout.
```
In case this occurs, please retype the query.
  

Some sample queries/inputs it can process are:
1. Greetings like “Hi”, “Hello”, “Hey there” and similar simple greetings.
2. Expressing a field of interest to get names of related labs
     Eg. “I would like to know about labs related to biometrics.” Or
           “Is anyone at GeorgiaTech working on graphics?”
3. Ask about faculty members at a lab
     Eg. “Who works at the PIXI Lab?” Or
           “Who are the faculty in Networks Lab?”
4. Ask more information about a lab
     Eg. “What is ADAM Lab?” Or
           “Can you tell me more about Contextual Computing Group?” Or
           “I want to know more about Sonification Lab.”
5. Ask which labs are associated with which faculty
    Eg. "What labs is Ashok Goel associated with?"
6. Ask more information about the lab in context
    Eg. "Can you tell me more about this lab?"