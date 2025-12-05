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
 - Portfolio Simulation
 - Volatility surface 
 - Ticker Price 
 - Ticker Financials Info
 - Yahoo Finance and Barchart sources
 - ... 
 
 Install dependency
  ```
   ./install.sh
 ```
 Run the Protype
 ```
  poetry run python -m prototype 
    --ticker  "AAPL" 
    --action "price" 
    --start_date "01/01/2008" 
    --end_date "01/01/2009" 
    --frequency "B"
    --source "yahoo"  
    --currency "USD" 
    --output "./Output" 
    --save  
    --plot

```
Data and Plot are stored in the output folder.

Choice for ```action``` :
 - price 
 - pair
 - financials
 - portfolio
 - volatility_surface 

### Price
 Only FX asset as ```FX_USDEUR``` 
### Pair 
 Retrive and plot custom pairing, like SPX vs GOLD. 
 Syntax on the ticker paramter as ```SPX_GC```, using ```_``` delimeter.

### Frequency conventions

| Symbol |  Description           |
|:-----  |:----------------------:|
| B      | Business date          |
| WE     | Weekly End             |
| WS     | Weekly Start           |
| BME    | Business month end     |
| BMS    | Business month start   |
| BQE    | Business quarter end   |
| BQS    | Business quarter start |
| BYE    | Business year end      |
| BYS    | Business year start    |
