**Breweries Population & Route Analysis**

---

### Project Overview
This project explores the U.S. brewery landscape by blending Open Brewery DB location data with the 2024 U.S. Census population estimates. The notebook walks through cleaning the raw brewery records, aligning them with population figures, quantifying breweries per capita, and visualizing the results via static plots and interactive folium maps. It also tackles a traveling-salesperson-style routing problem—first on a Los Angeles subset, then (optional) between the northernmost brewery in Maine and the easternmost brewery in Hawai‘i—using a greedy path plus a Lin–Kernighan refinement pass. Generated plots land in `plots/`, and interactive maps are saved to `maps/` for easy sharing.

---

### Datasets & Citations
| File | Description | Source |
| --- | --- | --- |
| `data/united_states_breweries.csv` | U.S. brewery locations, types, and contact info (Open Brewery DB export). | Open Brewery DB. [https://www.openbrewerydb.org](https://www.openbrewerydb.org) |
| `data/SUB-IP-EST2024-ANNRNK.xlsx` | “Annual Estimates of the Resident Population for Incorporated Places of 20,000 or More, Ranked by July 1, 2024 Population.” Provides population, rank, and historical estimates for U.S. cities. | U.S. Census Bureau, Population Division (Release: May 2025). [https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html](https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html) |

Key characteristics:

- Brewery data includes ~8k rows that represent all register breweries within the USA, with columns for name, brewery type, city/state, coordinates, and contact metadata.
- Population data combines a two-row header and multiple yearly estimates; after cleaning we retain rank, city, state, and the July 1, 2024 estimate.
- Both datasets are stored locally under `data/`, and the notebook expects them in that relative path.

---

### Retrieve Brewery Data from the API
If you want the latest brewery snapshot (rather than using the CSV already in `data/`), run the helper script that calls the Open Brewery DB REST API and writes the results to disk.

```bash
cd Breweries_Data_Project
python data/import_breweries.py
```

The script pages through the `/v1/breweries` endpoint, filters for United States breweries, and saves the output to `data/united_states_breweries.csv`. You only need to run it when you want to refresh the dataset; subsequent notebook runs will reuse the saved CSV.

---

### Environment & Installation

1. **Clone the repository (or copy the project folder)**  
   ```bash
   git clone <your-fork-or-path>
   cd Breweries_Data_Project
   ```

2. **Create and activate a virtual environment (recommended)**  
   ```bash
   python3 -m venv env
   source env/bin/activate          # On Windows: env\Scripts\activate
   ```

3. **Install the required Python packages**  
   The notebook relies on pandas, NumPy, Matplotlib, Folium, scikit-learn, and tqdm. Install them with pip:
   ```bash
   pip install pandas numpy matplotlib folium scikit-learn tqdm jupyter
   ```

4. **Launch Jupyter**  
   ```bash
   jupyter notebook
   ```
   Open `EDA_breweries.ipynb` from the Jupyter interface.

---

### Running the Analysis (Notebook Walkthrough)
Open `EDA_breweries.ipynb` and execute the cells. Each major section contains markdown guidance and inline comments to clarify what’s happening.

1. **Setup**  
   - Imports pandas/NumPy/Matplotlib, Folium for mapping, scikit-learn for TF-IDF matching, and tqdm for progress bars.
   - Run the cell to confirm the environment is ready.

2. **Brewery Data**  
   - Loads `united_states_breweries.csv`.
   - Drops breweries marked as `closed`, `planning`, or `large`.
   - Leaves a filtered DataFrame (`df_clean`) for later steps.

3. **Population Data**  
   - Reads `SUB-IP-EST2024-ANNRNK.xlsx`.
   - Flattens the two-level header, isolates `Rank`, `Geographic Area`, and `Population 2024`.
   - Splits “Geographic Area” into `city` and `state`, yielding `population_df`.

4. **Breweries per City (TF-IDF Matching)**  
   - Normalizes city/state text.
   - Uses TF-IDF to match each brewery location to the best population entry when names differ.
   - Produces `breweries_per_city` with brewery counts and population stats; unmatched cities are listed for manual review.

5. **Population vs. Brewery Visualizations**  
   - **Breweries Per Capita**: calculates breweries per 100k residents; displays top/bottom tables.
   - **Hexbin Density**: shows population vs. brewery count density; saved as `plots/population_vs_breweries_hexbin.png`.
   - **Log-Log Scatter**: same relationship on log scales; saved as `plots/population_vs_breweries_loglog.png`.
   - **Population Band Summary**: buckets cities by population and plots average brewery counts as bar chart; saved as `plots/average_breweries_population_band.png`.
   - **Brewery Density Heatmap**: per-capita intensity on a Folium map; saved as `maps/brewery_heatmap.html`.
   - **Correlation & Residual Analysis**: prints Pearson/Spearman correlations, displays residual stats, and saves `plots/population_vs_breweries_residuals.png`.

6. **Geo Cleanup & Full Brewery Map**  
   - Converts coordinates for location dataframe to numeric.
   - Drops rows outside a broad U.S. bounding box.
   - Plots every remaining brewery on a Folium map saved as `maps/all_breweries_map.html`.

7. **Los Angeles Demo**  
   - Filters `df_geo` (post-cleanup) to Los Angeles.
   - Runs the TSP-style path builder between the northernmost and southernmost LA breweries.
   - Displays route stats and saves an interactive `la_route_map.html` with beer-mug markers.

8. **Northern Maine to Eastern Hawaii Path**  
   - Identifies the endpoints in Maine and Hawaii.
   - Runs `build_brewery_path` to compute a TSP-style route across all breweries (greedy pass with Lin–Kernighan refinement).
   - Produces a pandas DataFrame with each stop’s “closest_brewery” and distance to the next leg.
   - (Leave the full run commented if you only want the LA demo; the US-wide path can take several minutes to finish.)

9. **Outputs**  
   - Re-running the plotting or mapping cells generates/updates the artifacts under:
     - `plots/` (PNG images)
     - `maps/` (HTML folium maps)

---

### Reproducing the Study From Scratch

1. **Retrieve brewery data (optional refresh)**  
   ```bash
   python data/import_breweries.py
   ```

2. **Place datasets**  
   Ensure `data/united_states_breweries.csv` and `data/SUB-IP-EST2024-ANNRNK.xlsx` exist relative to the repository root.

3. **Set up the Python environment**  (see installation steps above).

4. **Run the notebook cells sequentially**  
   - Watch the markdown cells—they summarize the goal of each block.
   - Stop after each major section to inspect the tables, charts, or saved artifacts if desired.
   - If you plan to regenerate maps, confirm the notebook has write access to `maps/` and `plots/`.

5. **Inspect the outputs**  
   - Static plots: `plots/*.png`
   - Interactive maps: open the HTML files in a web browser (e.g., `open maps/la_route_map.html` on macOS/Linux or double-click in Finder/Explorer).

6. **Optional extensions**  
   - Swap the LA start/end indices to experiment with different routes.
   - Adjust TF-IDF thresholds if cities remain unmatched.
   - Re-run the per-capita analysis for specific states or metropolitan areas by filtering `breweries_per_city`.

Following these steps from a clean clone will reproduce the entire exploratory analysis, mapping workflow, and pathfinding results captured in `EDA_breweries.ipynb`.
