```
Write query for listing requirement and snapshot the result (run time and execution plan)
    1. Total revenue per month
    2. Orders filtered by seller and date
    3. Filter data in `order_item` by product_id
    4. Find order with highest total_amount
    5. List products with highest quantity sold
    6. Orders by Seller in October
    7. Revenue per Product per Month
    8. Products Sold per Seller
- Create monthly partitions for the two tables above and create an index on the `product_id` column of `order_item` table.
- Write query for above requirements again and snapshot the result (run time and execution plan); then compare
```

![img.png](images/data_gen.png)


#### 1. Total revenue per month
![query1_plan.png](images/q1_plan.png)
![query1_analyze.png](images/q1_analyze.png)
After:

#### 2. Orders filtered by seller and date
![q2_plan.png](images/q2_plan.png)
![q2_analyze.png](images/q2_analyze.png)

#### 3. Filter data in `order_item` by product_id
![q3_plan.png](images/q3_plan.png)
![q3_analysis.png](images/q3_analysis.png)

#### 4. Find order with highest total_amount
![q4_plan.png](images/q4_plan.png)
![q4_analysis.png](images/q4_analysis.png)

#### 5. List products with highest quantity sold
![explain_plan_1771604702752.svg](images/q5_explain_plan_1771604702752.svg)
![q5_plan.png](images/q5_plan.png)
![q5_analysis.png](images/q5_analysis.png)
#### 6. Orders by Seller in October
![q6_explain_plan_1771605249782.svg](images/q6_explain_plan_1771605249782.svg)
![q6_plan.png](images/q6_plan.png)
![q6_analyze.png](images/q6_analyze.png)

#### 7. Revenue per Product per Month
![q7_explain_plan_1771605498713.svg](images/q7_explain_plan_1771605498713.svg)
![q7_plan.png](images/q7_plan.png)
![q7_analysis.png](images/q7_analysis.png)

#### 8. Products Sold per Seller
![q8_explain_plan_1771605676335.svg](images/q8_explain_plan_1771605676335.svg)
![q8_plan.png](images/q8_plan.png)
![q8_analysis.png](images/q8_analysis.png)
