#########
Structure
#########


Make and Use Framework
----------------------

The general idea for the hybridization is to distinguish between a foreground and a background system.
Each system is characterized by it's own make and use tables.
The forground system and the background system are represented by a make table (:math:`\mathbf{V}_{for}` and :math:`\mathbf{V}_{back}`, respectively) and a use table (:math:`\mathbf{U}_{for}`  and :math:`\mathbf{U}_{back}`, respectively).

The aim is to combine both systems so that no double-counting occurs. Special emphasize is thus needed for the use table :math:`\mathbf{U}`.

To connect both systems properly, co-called cut-off matrices :math:`\mathbf{C}_{u}` and :math:`\mathbf{C}_{d}` are introduced. :math:`\mathbf{C}_{u}` connects the upstream processes of the foreground system to the industries of the background system. :math:`\mathbf{C}_{d}` connects the downstream industries to the processes of the foreground sytem.

The hybridized total system represented by :math:`\mathbf{V}` and :math:`\mathbf{U}` includes all necessary adoptions of the submatrices and avoids double-counting.    

.. math::
   \begin{array}{lccccccc} \hline
    &  \textit{Commodities} & 	& \textit{Industries} &  & & \\
   \hline
   \textit{Commodities} & & & \mathbf{U}_{for} & \mathbf{C}_{d}^{*} & \mathbf{e}_{for} & \mathbf{q}_{for}\\
		                & & & \mathbf{C}_{u}^{*} & \mathbf{U}_{back} & \mathbf{e}_{back} & \mathbf{q}_{back}\\
		                & & & \textbf{Use matrix} & & \textbf{Final demand} & \textbf{Total output}\\
		                \\
   \textit{Industries}     & \mathbf{V}_{for} & 0 & & & & \mathbf{g}_{for}\\
		                & 0 & \mathbf{V}_{back} & & & & \mathbf{g}_{back}\\
		                & \textbf{Make matrix} & & & & & \textbf{Total output}\\
		                \\
                                 & & & \mathbf{v'}_{for} & \mathbf{v'}_{back} &  & \\
		                & & & \textbf{Value added} & & \\
		                \\
                                & \mathbf{q'}_{for} & \mathbf{q'}_{back} & \mathbf{g'}_{for} & \mathbf{g'}_{back} & & \\
	                	     & \textbf{Total inputs} & & \textbf{Total inputs} & & \\		
		     \\				
   \hline
   \textit{Interventions}  &  &  & \mathbf{F}_{for} & 0 & & \\
                               &  &  & \mathbf{F}_{u}^{*} & \mathbf{F}_{back} & & \\
		              &  &  & \textbf{Factor matrix} & & \\
   \end{array}

Furthermore, additional factors can be taken into account which are represented by the intervention matrix :math:`\mathbf{F}`.

To re-allocate the interventions from the industries of the background system to the foreground system, a sub-matrix :math:`\mathbf{F}_{u}` is introduced.

NOTE: An additional sub-matrix is thinkable to re-allocate interventions the other way around, but is not yet implemented. The intervention tables might be in principle  also defined per commodity



Data format
-----------

The hybridvut package uses `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_ to deal with the required matrices. The format of these DataFrames needs to fulfill certain requirements in regard to its `pandas.MultiIndex <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.MultiIndex.html>`_. 

A system based on the make and use framework can consit of the following matrices.

.. csv-table:: Make matrix V
   :stub-columns: 2
   :header-rows: 3

   "", "region", "...", "...", "..."
   "", "commodity", "...", "...", "..."
   "", "unit", "...", "...", "..."
   "region", "industry", "", "", ""
   "...", "...", "v_1,1", "v_1,2", "..."
   "...", "...", "v_2,1", "v_2,2", "..."
   "...", "...", "...", "...", "..."

.. csv-table:: Use matrix U
   :stub-columns: 3
   :header-rows: 2

   "", "", "region", "...", "...", "..."
   "", "", "industry", "...", "...", "..."
   "region", "commodity", "unit", "", "", ""
   "...", "...", "...", "u_1,1", "u_1,2", "..."
   "...", "...", "...", "u_2,1", "u_2,2", "..."
   "...", "...", "...", "...", "...", "..."

.. csv-table:: Intervention table F
   :stub-columns: 2
   :header-rows: 2

   "", "region", "...", "...", "..."
   "", "industry", "...", "...", "..."
   "intervention", "unit", "", "", ""
   "...", "...", "f_1,1", "f_1,2", "..."
   "...", "...", "f_2,1", "f_2,2", "..."
   "...", "...", "...", "...", "..."

.. csv-table:: Characterization matrix Q
   :stub-columns: 2
   :header-rows: 2

   "", "intervention", "...", "...", "..."
   "", "unit", "...", "...", "..."
   "impact", "unit", "", "", ""
   "...", "...", "q_1,1", "q_1,2", "..."
   "...", "...", "q_2,1", "q_2,2", "..."
   "...", "...", "...", "...", "..."

