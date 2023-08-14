# An operational risk loss database of Chinese commercial banks from 1990 to 2023

This work is to constrcut the operational risk loss database automatically from Chinese news releases.

Operational risk, following credit risk and market risk, has been regarded as the third major risk that the banks are exposed to and covered under the capital adequacy requirements of Basel Accord II by the Basel Committee on Banking Supervision (BCBS). However, the absence of a public operational risk database, attributed to factors such as data privacy protection, insufficient quantity, and delayed updates from manual collection, has hindered comprehensive risk analysis.

In response to this gap, our study proposes a novel data collection framework that combines text mining methods to establish and publish one of the largest and most comprehensive external databases of cross-institution operational risk in academia. This Chinese Operational Loss Database(COLD) comprises 3,723 operational risk events related to Chinese commercial banks spanning from 1990 to 2023, named Public Chinese Operational Risk Loss Database(P-COLD). To provide a comprehensive description of these events, 17 fields, such as occurrence time, loss amount, and business line, are included. The characteristics of loss amount in this database, such as severity and frequency of events, align with the conclusions drawn from existing studies on operational risk data. We firmly believe that this database will facilitate operational risk capital calculations, event dependence analysis, textual analysis, and strengthening institutional internal controls within the banking sector.

If you want to constrcut the operational risk loss databse by youself, Please download all files and run the codes in the following order:

1-Operational Risk Events Selection.py

2-Key fields extraction based on named entity recognition method.py

3-1-Key fields extraction based on MLP-causal factor.py

3-2-Key fields extraction based on MLP-business line.py

3-3-Key fields extraction based on MLP-losstype.py

Note: Before you start, please prepare a raw news dataset like new_text_example.xlsx in this depot.For copyright reasons, we do not publish crawler codes.

Please do not hesitate to contact me if you have any queries about this work.
Email:changyanpeng19@mails.ucas.ac.cn
