# DeltaStream
---

In this data engineering project, I aimed to build a batch processing workflow using Airflow, Kafka, and Databricks. PowerBI was also used at the final stage to create an analysis dashboard. The OpenSky API for real time airplane data and the weather.gov API's were used in this workflow. The weather data from the weather API would be used in conjunction with the airplane data to factor in how weather patterns affect aircraft metrics such as speed and altitude.

</br></br>
### High Level Architecture
---
<img width="1156" height="301" alt="image" src="https://github.com/user-attachments/assets/d90b8790-6e6f-49f0-b18e-4242f3144226" />

</br>

This architecture consists of 2 Airflow DAGs. The Extract DAG runs every minute, and fetches the data from the APIs and stores it in respective Kafka topics. The Transform Load DAG ran a full medallion architecture pipeline in Databricks, and saved final Gold level aggregate views in AWS S3. Finally, the Load step in this DAG fetched the data from S3, enabling PowerBI to analyze and visualize the data. 

</br></br>

<img width="1279" height="774" alt="Screenshot 2025-08-29 005206" src="https://github.com/user-attachments/assets/2998bfae-f767-4543-a295-94c763144c5b" />

</br></br>
### Conclusion
---
Overall, this project served to offer fundamental experience in building an end-to-end data engineering workflow.
