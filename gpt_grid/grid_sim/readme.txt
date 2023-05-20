usage


>> main.exe -b batches.json

(create your own batches.json, and run

main.exe -b  <your file name>

eg  main.exe -b batch00.json

file is an array of packages 

[
{...},

{...}




]


each package has a package Uid and an array of trade uids

{Uid:17,
TradeUids: [1,2,99,543]
}

the union of all the TradeUids across packages should be 0....9999   (10^5 total trades)
