########################
Hybridization procedures
########################

hybridize()
-----------

Currently, only one hybridization procedure is implemented.
The steps of this procedure are as following.

#. Define concordance matrices :math:`\mathbf{H}`, :math:`\mathbf{H1}` and :math:`\mathbf{HF}` (for industries, commodities and interventions, respectively)
#. Adjust :math:`\mathbf{V}_{back}`, :math:`\mathbf{U}_{back}`; and calculate :math:`\mathbf{q}` and :math:`\mathbf{g}` based on :math:`\mathbf{V}`
#. Define weighting factor matrices :math:`\mathbf{T}` and :math:`\mathbf{T1}`
#. Calculate upstream cut-off matrix :math:`\mathbf{C}_{u}` and adjust :math:`\mathbf{U}_{back}` (second time)
#. Calculate downstream cut-off matrix :math:`\mathbf{C}_{d}` and  adjust :math:`\mathbf{U}_{back}` (third time)
#. Correct :math:`\mathbf{C}_{d}`, :math:`\mathbf{C}_{u}` and :math:`\mathbf{U}_{for}`
#. Adjust intervention sub-tables of :math:`\mathbf{F}`
#. Combine all submatrices into :math:`\mathbf{V}`, :math:`\mathbf{U}` and :math:`\mathbf{F}`
#. Adjust characterization matrix :math:`\mathbf{Q}`

Define concordance matrices
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`\mathbf{H}_{ind}` relates process of foreground system to industry of background system (includes 1 if relation, otherwise 0).
:math:`\mathbf{H}_{om}` relates commodity of foreground system to commodity of background system (includes 1 if relation, otherwise 0).
:math:`\mathbf{H}_{int}` relates an intervention of the foreground system to an intervention of the background system (includes 1 if relation, otherwise 0).
Note: in multi-regional models the relation is country-wise (e.g., a commodity of a country can only related to a commodity of one country). However, more than one industry of the background can be associated to the industry of the forground system (the same is true for the commodity relation). Thereby, the sum of all associated industries (commodities) must equal


.. csv-table:: Concordance matrix H_ind
   :stub-columns: 2
   :header-rows: 2

   "", "region", "...", "...", "..."
   "", "industry", "...", "...", "..."
   "region", "industry", "", "", ""
   "...", "...", "h_1for,1back", "h_1for,2back", "..."
   "...", "...", "h_2for,1back", "h_2for,2back", "..."
   "...", "...", "...", "...", "..."

.. csv-table:: Characterization matrix Q
   :stub-columns: 3
   :header-rows: 3

   "", "", "region", "...", "...", "..."
   "", "", "commodity", "...", "...", "..."
   "", "", "unit", "...", "...", "..."
   "region", "commodity", "unit", "", "", ""
   "...", "...", "...", "h1_1for,1back", "h1_1for,2back", "..."
   "...", "...", "...", "h1_2for,1back", "h1_2for,2back", "..."
   "...", "...", "...", "...", "...", "..."

.. csv-table:: Characterization matrix Q
   :stub-columns: 2
   :header-rows: 2

   "", "intervention", "...", "...", "..."
   "", "unit", "...", "...", "..."
   "intervention", "unit", "", "", ""
   "...", "...", "hf_1for,1back", "hf_1for,2back", "..."
   "...", "...", "hf_2for,1back", "hf_2for,2back", "..."
   "...", "...", "...", "...", "..."

Adjust V_back, U_back
~~~~~~~~~~~~~~~~~~~~~
.. math::

   \begin{eqnarray}
   \mathbf{U}_{back}^{adj} = \mathbf{U}_{back} - \mathbf{H}_{com}^{T} \cdot \mathbf{U}_{for} \cdot \mathbf{H}_{ind}^{T} \\
   \mathbf{V}_{back}^{adj} = \mathbf{V}_{back} - \mathbf{H}_{ind} \cdot \mathbf{V}_{for} \cdot \mathbf{H}_{com} \\
   \mathbf{g}_{for} = \mathbf{V}_{for} \cdot \mathbf{i} \\
   \mathbf{q}_{for} = \mathbf{V}_{for}^{T} \cdot \mathbf{i} \\
   \mathbf{g}_{back}^{adj} = \mathbf{V}_{back}^{adj} \cdot \mathbf{i} \\
   \mathbf{q}_{back}^{adj} = \mathbf{V}_{back}^{adj T} \cdot \mathbf{i} \\
   \end{eqnarray}

, where :math:`\mathbf{i}` is the summation vector of ones with prpoper lenght.

Define weighting factor matrices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Matrix :math:`\mathbf{T}_{u}` defines how much of the upstream input can be related to the foreground processes (and thus shifted from the background industries). Here, the assumption is made that this is determined automatically by the ratio of industry output x (of the new process and its reference industry).

Matrix :math:`\mathbf{T}_{d}` defines how much of the downstream input can be related to the foreground processes (and thus shifted from the background industries). Here, the assumption is made that this is determined by the ratio of commodity output q (of the new commodity and its reference commodity)

.. math::
   :nowrap:

   \begin{eqnarray}
   \mathbf{T}_{u} = \left[ \mathbf{J}_{c,i} \cdot \mathbf{H}_{ind} \cdot \mathbf{\hat{g}_{for}} \right]  \varnothing  \left[ \mathbf{J}_{c,i} \cdot \mathbf{H}_{ind} \cdot \mathbf{\hat{g}_{for}} + \mathbf{J}_{c,i} \cdot \mathbf{\hat{g}_{back}^{adj}} \cdot \mathbf{H}_{ind}  \right] \\
   \mathbf{T}_{d} = \left[  \mathbf{\hat{q}_{for}}  \cdot \mathbf{H}_{com} \cdot  \mathbf{J}_{c,i}  \right]  \varnothing  \left[ \mathbf{\hat{q}_{for}}  \cdot \mathbf{H}_{com} \cdot  \mathbf{J}_{c,i} + \mathbf{H}_{com} \cdot \mathbf{\hat{q}_{back}^{adj}}  \cdot \mathbf{J}_{c,i} \right]
   \end{eqnarray}

Calculate upstream cut-off matrix C_u 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. math::

   \begin{eqnarray}
   \mathbf{C}_{u} = \mathbf{T}_{u} \odot \mathbf{U}_{back}^{adj} \cdot \mathbf{H}_{ind} \\
   \mathbf{U}_{back}^{adj1} = \mathbf{U}_{back}^{adj} - \mathbf{C}_{u} \cdot \mathbf{H}_{ind}^{T} 
   \end{eqnarray}

Calculate downstream cut-off matrix C_d 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. math::

   \begin{eqnarray}
   \mathbf{C}_{d} = \mathbf{T}_{d} \odot \mathbf{H}_{com} \cdot \mathbf{U}_{back}^{adj1} \\
   \mathbf{U}_{back}^{adj2} = \mathbf{U}_{back}^{adj1} - \mathbf{H}_{com}^{T} \cdot \mathbf{C}_{d}
   \end{eqnarray}

Correct C_d, C_u and U_for
~~~~~~~~~~~~~~~~~~~~~~~~~~
The correction term :math:`\mathbf{O}_{u}` removes commodities those are actually covered as commodities in the foreground system.
The correction term :math:`\mathbf{O}_{d}` removes commodities those are actually used by technology of the foreground system.

.. math::

   \begin{eqnarray}
   \mathbf{C}_{u}^{adj} = \mathbf{C}_{u} - \underbrace{ \mathbf{C}_{u} \odot \mathbf{H}_{com}^{T} \cdot \mathbf{T}_{u} \cdot \mathbf{H}_{ind} }_{\text{correction term $\mathbf{O}_{u}$}} \\
   \mathbf{C}_{d}^{adj} = \mathbf{C}_{d} - \underbrace{ \mathbf{C}_{d} \odot \mathbf{H}_{com} \cdot \mathbf{T}_{d} \cdot \mathbf{H}_{ind}^{T}}_{\text{correction term $\mathbf{O}_{d}$}} \\
   \mathbf{U}_{for}^{adj} = \mathbf{U}_{for} + \mathbf{H}_{com} \cdot \mathbf{O}_{u} + \mathbf{O}_{d} \cdot \mathbf{H}_{ind}
   \end{eqnarray}

Adjust intervention sub-tables of F
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The re-allocation procedure is similar to the first steps of re-allocation the commodities from the background to the foreground system. The implicit assumption is (currently) that the background system already includes the intire interventions; and no additional interventions are added by the foreground system. The task hence is to remove the interventions of the associated processes from the background system to the foreground system, which are not yet taken into account in the foreground system

.. math::

   \begin{eqnarray}
   \mathbf{F}_{back}^{adj} = \mathbf{F}_{back} - \mathbf{H}_{int} \cdot \mathbf{F}_{for} \cdot \mathbf{H}_{ind}^{T} \\
   \mathbf{T}_{int} = \left[ \mathbf{J}_{c,i} \cdot \mathbf{H}_{ind} \cdot \mathbf{\hat{g}_{for}} \right]  \varnothing  \left[ \mathbf{J}_{c,i} \cdot \mathbf{H}_{ind} \cdot \mathbf{\hat{g}_{for}} + \mathbf{J}_{c,i} \cdot \mathbf{\hat{g}_{back}^{adj}} \cdot \mathbf{H}_{ind}  \right] \\
   \mathbf{F}_{u} = \mathbf{T}_{int} \odot \mathbf{F}_{back}^{adj} \cdot \mathbf{H}_{ind} \\
   \mathbf{F}_{back}^{adj1} = \mathbf{F}_{back}^{adj} - \mathbf{F}_{u} \cdot \mathbf{H}_{ind}^{T} \\
   \end{eqnarray}

Combine all submatrices
~~~~~~~~~~~~~~~~~~~~~~~
.. math::

   \begin{array}{lccccccc} \hline
    &  \textit{Commodities} & 	& \textit{Industries} &  & & \\
   \hline
   \textit{Commodities} & & & \mathbf{U}_{for}^{adj} & \mathbf{C}_{d}^{adj} & \mathbf{e}_{for} & \mathbf{q}_{for}\\
		                & & & \mathbf{C}_{u}^{adj} & \mathbf{U}_{back}^{adj2} & \mathbf{e}_{back}^{adj} & \mathbf{q}_{back}^{adj}\\
		                & & & \textbf{Use matrix} & & \textbf{Final demand} & \textbf{Total output}\\
		                \\
   \textit{Industries}     & \mathbf{V}_{for} & 0 & & & & \mathbf{g}_{for}\\
		                & 0 & \mathbf{V}_{back}^{adj} & & & & \mathbf{g}_{back}^{adj}\\
		                & \textbf{Make matrix} & & & & & \textbf{Total output}\\
		                \\
                                 & & & \mathbf{v'}_{for}^{adj} & \mathbf{v'}_{back}^{adj} &  & \\
		                & & & \textbf{Value added} & & \\
		                \\
                                & \mathbf{q'}_{for}^{adj} & \mathbf{q'}_{back}^{adj} & \mathbf{g'}_{for} & \mathbf{g'}_{back} & & \\
	                	     & \textbf{Total inputs} & & \textbf{Total inputs} & & \\		
		     \\				
   \hline
   \textit{Interventions}  &  &  & \mathbf{F}_{for} & 0 & & \\
                               &  &  & \mathbf{F}_{u}^{*} & \mathbf{F}_{back}^{ad1} & & \\
		              &  &  & \textbf{Factor matrix} & & \\
   \end{array}

Adjust characterization matrix Q
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To deal with the characterization factors of (environmental) interventions, currently, two alternatives are implemented:

* Characterisation factors are provided for the background system; or
* Characterization factors are provided for the foreground system

if :math:`\mathbf{Q}_{back}` is given:

.. math::

   \mathbf{Q}_{for} = \mathbf{Q}_{back} \cdot \mathbf{H}_{int}

if :math:`\mathbf{Q}_{for}` is given:

.. math::

   \mathbf{Q}_{back} = \mathbf{Q}_{for} \cdot \mathbf{H}_{int}^{T}


Further notes
~~~~~~~~~~~~~
The hybridization procedure for the messageix-exiobase example includes three modifications of these steps (necessary due to the nature of the messageix model):
1. Aggregating sectors (i.e., technologies those have "final" products as input flows) are set to zero. The use of these products is covered by the background system.
2. To ensure that value added is the same after hybridizarion, we use it from the background system (::math:`\mathbf{F}_{back}`), allocate it among the industries (i.e. foreground technologies) and resacle the make and use tables to fulfill the original Exiobase ratios of values added (:math:`\mathbf{v}_{back}_{i}`) per intermediate input (:math:`\sum_{c} U_{back}_{c,i}`) of the corresponding industry i.
3. Before allocating GHG emissions from background to foreground industries (step 7), the total GHG emissions (CO2, CH4, N20), are usd to scale the corresponding emissions in Exiobase. GHG emissions of the foreground system are then set to zero (:math:`\mathbf{F}_{for}`).
