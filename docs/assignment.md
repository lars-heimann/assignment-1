# First Assignment - Business Process Prediction, Simulation, and Optimization - Summer Semester 2026

**Instructions for the Process and Data Science Tasks on the BPIC-17 Event Log**

Chair of Information Systems and Business Process Management
TUM School of Computation, Information and Technology
Technical University of Munich

April 23, 2026

---

**Abstract** -- Summarize the task and the event log, describe your findings, and present your main results in 4-5 sentences.

## 1 Information

The **maximum page limit is 5 pages**, excluding references and the appendix. The **report must be written in English**.

### 1.1 Grading

Tasks are divided into *basic* and *advanced*. Completing only the basic tasks results in a grade between 4.0 and 2.0. Completing the advanced task (Section 3.4) can improve your grade to 1.0.

The evaluation criteria are:

- **Rigor:** Use appropriate and well-justified methods. Ensure your work is reproducible: share your code via a public GitHub or GitLab repository, document all parameters for machine learning models, and fix random seeds for data splits. Reference all sources, tools, and datasets properly: use footnotes for code, technical reports, and Python packages, and citations for scientific literature.
- **Presentation of Results:** Provide a clearly structured description that directly addresses each task. If you take any design decisions, justify them and discuss their advantages and limitations, especially for the process model design. Use precise, informative visualizations that directly support your analysis, e.g., for the simple and advanced event log analysis if appropriate.

### 1.2 Tooling

- **GenAI:** You may use any GenAI model for writing assistance, but you must include a usage declaration. You are responsible for all content. **Do not let a GenAI tool generate entire sentences or paragraphs; use it only to improve precision and clarity.**
- **Open-Source Tools and Copilot:** You may use any open-source tool or library. Add a footnote with a link for each one. You may use Copilot (GenAI), but you must include a usage declaration.
- **Commercial Tools:** You may use commercial software, e.g., Celonis, SAP Signavio (not the academic version), for visualization. Include a list of all commercial tools used and provide screenshots of results. If you use commercial software to compute quality metrics, you must also provide a Python reimplementation.

## 2 Introduction

Write a brief introduction to your report based on external sources and your own findings. Describe the event log: its application domain, when and why it was generated, and what business process it captures. Reference existing reports and their key insights (e.g., from https://ais.win.tue.nl/bpi/2017/challenge.html).

## 3 Approach and Results

Present your analysis approach, results, and visualizations. Include the link to your publicly accessible GitHub or GitLab repository. Insert your final process model as a BPMN 2.0 (we recommend the figure as a PDF).

### 3.1 Technical Setup and Preliminaries

Describe your technical setup: Python libraries used, visualization techniques, and process modeling tools. Provide a footnote for each package, library, and tool.

### 3.2 Simple Event Log Analysis

Report basic event log statistics in a table, including:
- Number of cases
- Number of events
- Number of process variants
- Number of distinct case and event attribute labels
- Mean and standard deviation of case length
- Mean and standard deviation of case duration (in days, minutes, and seconds)
- Number of categorical event attributes

Provide at least two additional statistics of your choice. Here, you can also consider statistics that can be visualized in diagrams.

### 3.3 Process Model Creation and Validation

Discover, refine, and evaluate a process model from the BPIC-17 event log that satisfies the four quality dimensions (fitness, precision, generalization, simplicity):

1. Apply at least two different process discovery algorithms and add the resulting process models in the appendix.
2. Compute all relevant PM4Py quality metrics. In addition, implement at least two simplicity metrics yourself in Python [1]. Report the result on all discovered process models.
3. Construct a final process model by combining insights from the discovery algorithms, existing reports, domain knowledge, and the simple event log analysis. Refine the model iteratively and explain your design decisions step by step. The model should replay approximately 80% of the cases while maintaining high precision, generalization, and simplicity. Discuss the rationale behind your modeling decisions and the limitations of the resulting model. Describe the trade-offs between the quality metrics, justify which metrics you prioritized, and explain why these are appropriate given that the model serves as a base model for simulation. Provide the resulting BPMN 2.0 process model in the report, along with the values for all quality metrics.
4. Perform data-aware process mining, also known as decision mining [2]. For each XOR in your final process model, add a decision block. Follow the instructions and approach of the paper. Find a way to visualize the BPMN in your report, including the decision blocks at the XOR gateways.

### 3.4 Advanced Analysis

Ground your analyses in a real, meaningful problem in the context of business process simulation. Formulate hypotheses that are genuinely interesting from a prediction, simulation, or optimization perspective, and clearly motivate why each addresses a question worth answering, i.e., what actionable insight does it provide?

Perform one analysis. For each analysis, address the following three points:

1. **Hypothesis:** State your research question and hypothesis. Explain why this scenario is relevant as input to a prediction or simulation model.
2. **Approach and Result:** Describe your method, present your results, and provide clear visualizations.
3. **Interpretation:** Explain how the results help for upcoming prediction, simulation, or optimization tasks.

Example analysis topics:

- **Data drift:** Analyze distributional shifts in continuous attributes (consider time series methods) and concept drift in the process [4]. What is the difference between distributional and concept drift in process science?
- **Clustering:** Apply unsupervised learning (e.g., K-means) with a clearly defined goal, such as identifying patterns across process variants.
- **Social network mining:** Apply social network mining to the resource data in the event log [3]. Find out how resources work together, and which data are exchanged between resources?
- **Machine learning applications and feature importance:** Find a suitable machine learning application that is valuable for business process simulation, train a model, and investigate which features drive predictions using XAI techniques such as SHAP on a trained neural network.
- Feel free to perform your own analysis idea...

A comparison of your results with insights from a commercial tool also counts as one advanced analysis.

## References

1. Josep Carmona, Boudewijn F. van Dongen, Andreas Solti, and Matthias Weidlich. *Conformance Checking - Relating Processes and Models*. Springer, 2018.
2. Massimiliano de Leoni and Wil M. P. van der Aalst. Data-aware process mining: discovering decisions in processes using alignments. In *Proceedings of the 28th Annual ACM Symposium on Applied Computing, SAC '13, Coimbra, Portugal, March 18-22, 2013*, pages 1454-1461. ACM, 2013.
3. Henryk Mustroph, Karolin Winter, and Stefanie Rinderle-Ma. Social network mining from natural language text and event logs for compliance deviation detection. In *Cooperative Information Systems - CoopIS*, volume 14353, pages 347-365. Springer, 2023.
4. Denise Maria Vecino Sato, Sheila Cristiana De Freitas, Jean Paul Barddal, and Edson Emilio Scalabrin. A survey on concept drift in process mining. *ACM Comput. Surv.*, 54(9):189:1-189:38, 2022.
