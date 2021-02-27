# Literature research: Discrete event modelling

**Author**: Milos Dragojevic
**Date**: October 31st 2019

## About

This document contains a series of summaries of papers. The subject of these papers is related to discrete event modelling. The summaries should present new insights into discrete event modelling, improving its understanding.

## Papers

### Sanford, A. D. & Moosa, I. A. (2012). A Bayesian network structure for operational risk modelling in structured finance operations. _The Journal of the Operational Research Society_, _63_ (4), pp.431-444

#### This paper seems very useful for the study that we are trying to perform.

This paper is concerned with the design of a Bayesian network structure that is suitable for operational risk modelling.  

Bayesian networks are ideal for analysing an event that occurred and predicting the likelihood that any one of several possible known causes was the contributing factor.

The model's structure is designed specifically from the perspective of a business unit operational risk manager whose role is to measure, record, predict, communicate, analyse and control operational risk within their unit.

The problem domain modelled is a functioning structured finance operations unit within a major Australian bank.
The network model design incorporates a number of existing human factor frameworks to account for human error and operational risk events within the domain. The design also supports a modular structure, allowing for the inclusion of many operational loss event types, making it adaptable to different operational risk environments.

This last paragraph is intriguing since we want to model a banking system where many potential events could occur and need to be taken into consideration. The problems that they encountered are:

- Payments made to incorrect beneficiaries, and/or for an incorrect amount, and/or for an incorrect value date. 
- Regulatory breach such as regulatory reporting or account segregation.
- Failure to enforce its rights or meet its obligations to counterparties over the life of a deal. 
- Exposure capture. This is the risk that the terms of a transaction or details of a counterparty /security are not recorded accurately in the Bank's systems, resulting in a misunderstanding of the risk profile.

#### The Bayesian network construction process is made in steps and cycles.

- Step 1, Structural development and evaluation:

    -  identify all of the relevant risk driver events, their causal relations, and the query, hypothesis or operational loss event variables.

- Step 2, Probability elicitation and parameter estimation:

    -  involves defining the probability distributions of the nodes and setting their parameter values.

- Step 3, Model validation:

    - **most problematic step**
    -  How does one validate a model constructed largely through the subjective opinion of experts?
        - Elication review
        - sensitivity analysis
        - case evaluation


#### Structural development

- What operational risk queries should the model be able to answer?
- What operational risk categories and events should be included in the model?
- What are the main risk drivers in SFO for operational risk events?
- What are the causal relations between risk drivers and risk events? 
- What are the key performance indicators (KPIs) for the SFO domain?

The paper developed a network structure for the modelling of operational risk based on a functioning SFO unit within a major Australian bank.
The dominant perspective used in developing this model structure is that of human error and its role in contributing to operational losses. Within the unit under investigation, human action plays a dominant role in the transaction processes, which makes it logical to emphasize human error.

The model is designed to generate probabilities of operational loss events by consideration of interaction between the working environment, transaction processes and their effect on the generation of human errors. A valuable feature of the model is its modularity, which provides the opportunity to add other types of operational loss events as necessary.


### Babulak, E., & Wang, M. (2008 ). Discrete Event Simulation _International Journal of Online Engineering (iJOE)_. _4_ (60)

Managers have started to use discrete event simulation for the service industries. In particular for banking and finance services. Some examples are:

- call center modeling & simulation
- bank branch modeling & simulation
- simulation of vehicle routing (cash carriage services) and number of cash carriage services per routing
- simulation study of cash management of ATM such as minimum re-order point, optimum budget and so on.

#### Modeling of service operations steps

**1)** Process flow: A manufacturing process is always associated with physical flows of
materials/components and therefore can be easily identified. It may not be the case for
many service applications where business activities are information-based and triggered by
an external or internal event such as a written or oral request. The current solution is to use
a business process mapping tool to capture the business process and then convert the
process model to the discrete event simulation model.

**2)** Process related data such as processing time: In a manufacturing company, industrial
engineers are responsible for time study, setting processing time and balancing flow. Most
of service companies do not hire industrial engineers or have equivalent position within
organizations. As a result, much of the process related data are not readily available.

**3)** Knowledge workers: In many service companies, employees work primarily with
information or develop and use knowledge. They are knowledge workers, a term coined by
Peter Drucker. A knowledge worker tends to be self-motivated, work interactively and
make decisions constantly. How to represent knowledge workers and human-decision
making process in discrete event simulation remains a subject under study.


### Davoli G., Nielsen P., Pattarozzi G., Melloni R. (2013) Practical Considerations about Error Analysis for Discrete Event Simulations Model.

#### https://www.mendeley.com/viewer/?fileId=30051a54-4770-bce3-1456-1504409a87ab&documentId=c7e181d3-64ce-34ec-8ee0-0e4148d1d8b4

#### This paper seems very useful for the study that we are trying to perform.

#### 

### Intro

Stochastic, discrete events, simulation models are widely used to study production and logistic system. Apart from the development, one of the main problem of this approach is to perform the error analysis on the outputs of the simulation model

If we limit our interests on non-terminating simulation, the error analysis can be split into two different parts. The first part consists of individuating the initial transient period and the confidence interval of the outputs. The second part consists of estimating how the transient period and the outputs confidence interval varies when the initial model scenario is changed.

The first part of the problem is widely studied.
Between the proposed techniques Mean Squared Pure Error method, Mosca et al. (1985-1992), should be reminded as a practical method useful to determinate both transient period  and confidence interval.

On the other hand the second part of error analysis problem is not commonly addressed. In fact in some recent simulation handbook (Chung 2004) the advice to quantify the confidence interval for all different simulated scenario is given.

### Method

The aim of this paper is to give some practical guidelines in order to drive the error analysis for discrete event stochastic simulation models. The paper is focused on the study of confidence interval variance related to the variance of simulated scenario. Nowadays, in many practical applications, the calculation potential is large enough to perform “long” simulation run in order to assure to exceed the initial transient period. Much more important is to determinate the confidence interval for the outputs in  different simulated scenario, because overestimate or underestimate these confidence intervals can drive analysts towards a wrong interpretation of the results. 

To address the aim of the paper a quite simple discrete event simulation model is considered and the MSPE (1) is used to es timate outputs confidence interval. Then the simulation are performed according to different scenario and the variance of confidence interval is studied for different outputs.

#### 3.1 Simulation Model 

The simulation model was developed according with the standard EOQ model for single item. A set of stochastic functions, developed in SciLab environment, are used to generate the demand that activates the model. The simulation model was tested performing standard EOQ model with normal distributed demand (where σd  is demand standard deviation) and normal distributed lead time (where σt  is lead time standard deviation).

To evaluate model performances, in terms of achieved service level, a set of  4 Key Performance Indicators (KPI) is defined.

#### 3.2 Design of the Experiments  

To investigate the influence of different parameters on confidence intervals four factors are considered. These four factors are: 
    • Demand distribution; 
    • Lead time distribution; 
    • Ratio Co/Cs ; 
    • SS, safety stocks. 

### Findings

In practice, the effort to check the confidence interval related to discrete event simulation should be done when the modified parameters are not simply numeric. This kind of analysis, thanks to the actual computational resource, is not prohibitive in terms of time when we manage a rather simple model.