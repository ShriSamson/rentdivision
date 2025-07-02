# rentdivision
A streamlit app based on acritch's rental harmony algorithm which allows prices to be input from a google sheet or manually.

Hosted at [rentdivision.streamlit.app](https://rentdivision.streamlit.app/)

## Instructions

Enter the names for the housemates and rooms, and have each housemate privately identify his/her least favorite room and write down a bid of $0 for that room. Next, have them privately write down how much extra they'd be willing to pay monthly (assuming they're playing close-to-average rent) for each other room. Then, reveal those values, enter them into the Marginal Values table below, and click "Calculate".

## Understanding the Results

**Envies Table:** The Envies table is an estimate of how much the prices would have to change for a housemate to prefer a given room over their assigned room. Greater magnitudes indicate a larger price change needed in order to be envious, smaller negative values indicate someone is likely to be envious if only a small change in price or change in circumstance occurs.
