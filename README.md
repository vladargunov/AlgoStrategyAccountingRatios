# Algorithmic Trading using Accounting Ratios

The current report intends to analyse how the ideas outlined in Olson, Mossman (2003)[^1] can be applied to the modern dataset of Chinese stocks available at [Kaggle](https://www.kaggle.com/datasets/franciscofeng/augmented-china-stock-data-with-fundamentals). All the available details can be found in the [report](report.pdf) file within the repo.

[^1]: Olson, Dennis \& Mossman, Charles. (2003). Mossman, Neural Network Forecasts of Canadian Stock Returns using Accounting Ratios. International Journal of Forecasting. 19, 453-465. International Journal of Forecasting. 19. 453-465.


## Usage

1. Clone the repo and navigate to the root of it

2. Make a directory named data and download two files from Kaggle *[Augmented Chinese Stock Data w/ FRs & Fundamentals](https://www.kaggle.com/datasets/franciscofeng/augmented-china-stock-data-with-fundamentals)* dataset and place them into the created folder.

3. Given the system has [Conda](https://docs.conda.io/en/latest/) installed, navigate to the project root directory and execute the following script

```bash
source ./build_environment.sh
```

4. If you wish to replicate the results of the [report](report.pdf), execute the following script

```bash
source ./report.sh
```

5. If you wish to perform your own analysis (using jupyter notebooks), execute this script

```bash
jupyter notebook
```

6. If you wish to work in the Docker environment of jupyter notebooks, execute this script, also changing the FULL_PATH_TO_PROJECT to your path

```bash
docker build -f Dockerfile -t strategy-ratios . \
&& docker run -it -p 8888:8888 -v {FULL_PATH_TO_PROJECT}:/home/jovyan/work/strategy-ratios strategy-ratios
```

You are all set! Now you can run the strategies from the paper with custom parameters (Exact manual how to do that will be added later :) )

I would appreciate any contribution, advice, or feedback from you about this project. Please do it within the framework of Github or email directly me via argunovvlad5@gmail.com

Hope I did better for the community!
