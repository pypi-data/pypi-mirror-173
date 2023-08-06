# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iterative_stats', 'iterative_stats.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0', 'pyyaml==6.0']

setup_kwargs = {
    'name': 'iterative-stats',
    'version': '0.0.2',
    'description': 'This package implements iterative algorithms to compute some basics statistics',
    'long_description': '# BasicIterativeStatistics\nIn this repository, basic iterative statistics are implemented.\n\n\n## Iterative statistics\n\nIn this repository, we implement the following basic statitistics:\n- Mean (see example [here](tests/test_IterativeMean.py))\n- Variance (see example [here](tests/test_IterativeVariance.py))\n- Extrema (see example [here](tests/test_IterativeExtrema.py))\n- Covariance (see example [here](tests/test_IterativeCovariance.py))\n\nWe detail in the [docs](docs/) folder the computation for each statistic:\n- [mean](docs/mean.md)\n- [covariance](docs/covariance.md)\n- [sobol](docs/sobol.md)\n\n## Additional info\nL\'implémentation des formules itératives s\'appuient sur les papiers suivant :\n- Dans [[3]](#3), l\'auteur propose une méthode permettant d\'évaluer la covariance (§3) de manière itérative. Un rappel est également fait sur la manière de calculer la moyenne (§1) et tous les moments d\'ordre supérieurs dont la variance (§2)\n- Dans [[2]](#2), les auteurs effectuent une revue des différents estimateurs permettant de calculer les indices de Sobol\n- [[1]](#1) est le papier MELISSA. En ce qui concerne les statistiques itératives, les méthodes employées sont rappelées en §3 \n\n\n\n\n\n## References \n<a id="1">[1]</a>  Théophile Terraz, Alejandro Ribes, Yvan Fournier, Bertrand Iooss, and Bruno Raffin. 2017. Melissa: large scale in transit sensitivity analysis avoiding intermediate files. In Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis (SC \'17). Association for Computing Machinery, New York, NY, USA, Article 61, 1–14. https://doi.org/10.1145/3126908.3126922\n\n<a id="2">[2]</a> M. Baudin, K. Boumhaout, T. Delage, B. Iooss, and J-M. Martinez. 2016. Numerical stability of Sobol\' indices estimation formula. In Proceedings of the 8th International Conference on Sensitivity Analysis of Model Output (SAMO 2016). Le Tampon, Réunion Island, France.\n\n<a id="3">[3]</a> Philippe Pébay. 2008. Formulas for robust, one-pass parallel computation of covariances and arbitrary-order statistical moments. Sandia Report SAND2008-6212, Sandia National Laboratories 94 (2008).\n\n\n',
    'author': 'Frederique Robin',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
