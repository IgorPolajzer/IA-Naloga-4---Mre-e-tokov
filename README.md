# Izbrani algoritmi  - Naloga 4 - Mreže tokov (Ford Fuelkerson/Edmonds Karp)

Pri tej nalogi sem implementiral algoritem iskanja največjega toka v grafu z uporabo postopka Ford Fuelkers.

## Analiza

Meritve so bile izvedene za deset različnih velikosti grafov, pri čemer je bila vsaka velikost testirana na desetih različnih naključno generiranih grafih. 
Za zmanjšanje vpliva merilnega šuma je bila vsaka meritev izvedena desetkrat, končni čas izvajanja pa je bil določen kot povprečje teh ponovitev.

![time_vs_nodes_edmonds_karp_(bfs).png](images%2Ftime_vs_nodes_edmonds_karp_%28bfs%29.png)

![time_vs_nodes_ford_fulkerson_(dfs).png](images%2Ftime_vs_nodes_ford_fulkerson_%28dfs%29.png)

![time_vs_edge_count_edmond_karps_(bfs).png](images%2Ftime_vs_edge_count_edmond_karps_%28bfs%29.png)

![time_vs_edge_count_ford_fuelkerson_(dfs).png](images%2Ftime_vs_edge_count_ford_fuelkerson_%28dfs%29.png)
