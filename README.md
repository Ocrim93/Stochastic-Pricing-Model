# Stochastic-Pricing-Model

## Vanilla-and-Exotic-Option-Pay-off
Monte Carlo program which uses a polymorphic class to determine the pay-off of the Vanilla and Exotic  options to be priced.

How inheritance could be used to implement a PayOff class that is closed for modification but open for extension.

Key ingredients:
  - Using a pay-off Abstract class (as interface) allows to add extra forms of pay-offs without modifying our Monte Carlo routine;
  - By overloading the operator() we can make an object look like a function;
  - const attribute makes our program faster and forces the coder to be aware of which code is allowed to change things and which code cannot;
  - Strike prices and Lower and Upper bound are private data which help us to separate interface from implementation. 


 Virtual method Benefits:
 
- Program is much clearer; 
- Extra functionality dependent on the pyaoff options.
    
    
 Implemented Options:
  - European Call Option 
  - European Put Option
  - Double Digital Option  

## Prototype

Prototype to fetch and compute:
 - Volatility surface 
 - price underlying
 - financials info
 - Risk-free rate from SOFR 
 - Yahoo Finance and Barchart sources
 - ... 
 
 Install dependency
  ```
   ./install.sh
 ```
 Run the Protype
 ```
  python -m prototype \
    --ticker  "AAPL" \
    --action "price" \
    --start "01/01/2008" \
    --end "01/01/2009" \
    --source "yahoo"  \
    --output "./" \
    --save True \
```


