# DEAP Sample: One Max Problem
[DEAP原文链接](http://deap.readthedocs.io/en/master/examples/ga_onemax.html)
[TOC]

本文是一个十分简单的入门任务。这个任务是求一个元素为0或1构成的数组的和的最大值。显然当元素全部为1的时候，数组的和有最大值，即为其长度。


<a name="setting-things-up"></a>
## Setting Things Up
首先，导入一些模块
```python
import random

from deap import base
from deap import creator
from deap import tools
```

<a name="creator"></a>
## Creator
creator是一个类工厂，可以在运行是构建新类。第一个参数是新类名称，第二个参数是所继承的基类，之后的参数是新类的属性。
```python
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
```
首先，定义一个FitnessMax类。它继承于deap.base模块的Fitness类。其还包含一个额外的属性weights。weights是一个元组(1.0,)，意思是我们将最大化单一的目标值。

然后，定义一个Individual类。它继承list类并且使fitness这个属性等于之前我们定义的fitnessMax。要注意的是，所有在creator容器创建的类都可以直接调用。

<a name="toolbox"></a>
## Toolbox
现在，我们自定义一些类来创建个体和种群。

我们将使用到的，如个体、种群、函数、操作符、参数等等，都是在Toolbox里面存储。添加和删除分别为register()和unregister()。
```python
toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
```
第一句创建一个toolbox类。

然后注册一个生成函数toolbox.attr_bool()。该函数被调用的时候，会随机产生为0或1。接下来的两个函数就是个体和种群的实例。

新函数在toolbox中注册只将别名与已经存在的函数相关联，并冻结部分参数。例如attr_bool()，它与randint()关联并设定里面两个参数a=0和b=1，意思是返回$a\le n \le b$中的整数n，也就是0,1。

个体是由函数initRepeat()产生。它的第一个参数是一个容器类,在我们的例子中 Individual是我们在前一部分中定义的。这个容器会用方法attr_bool()填充。调用的时候，individual()方法将用attr_bool()初始化100次，然后产生一个个体。最后，population()用相同方法生成。

<a name="the-evaluation-function"></a>
## The Evaluation Function
评价函数。

```python
def evalOneMax(individual):
    return sum(individual),
```
简单地求和最大值。

<a name="the-genetic-operators"></a>
## The Genetic Operators
遗传算子。

在DEAP有两种方法使用算子。我们可以简单地调用tools模块中的函数，又或者，在toolbox里面注册。最方便的方法是注册，因为其可以允许我们容易地切换算子。

注册如下
```python
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
```
评价函数将采用别名来调用。稍后我们将需要在种群中每一个个体应用函数。突变要把一个参数固定下来。

<a name="evolving_the_population"></a>
## Evolving the Population
进化。

选择好算子后，我们将定义一个进化算法来解决我们的问题。

<a name="creating-the-population"></a>
### Creating the Population
首先，我们实例化我们的种群。
```python
def main():
    pop = toolbox.population(n=300)
```
pop是一个有300个体的list。由于我们没有固定种群的数量，所有可以自由创建任意数量。

下一步，评价新种群
```python
  # Evaluate the entire population
  fitnesses = list(map(toolbox.evaluate, pop))
  for ind, fit in zip(pop, fitnesses):
      ind.fitness.values = fit
```
利用map()计算每个个体的评价函数。然后分配到各自的适合度中。

定义一些常量。
```python
    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2
```

<a name="performing-the-evolution"></a>
### Performing the Evolution
执行进化。

要做的是获得个体的适应度。
```python
    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]
```
进化我们的种群直到其中一个个体达到100或者世代数到1000
```python
    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while max(fits) < 100 and g < 1000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)
```
进化是由选择、交配、变异个体来进行的。

在这个例子中，第一步是选择下一代。
```python
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
```
这创建了一组后代。toolbox.clone()方法确保我们将使用一个完全独立的实例引用。这是十分重要的，因为算子会直接修改提供的对象。

然后，根据概率CXPB和MUTPB来交配和变异产生的后代。
```python
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
```
交配和变异的算子通常是2个或1个个体作为一个输入，返回2个或1个修改过的个体。除修改过的个体，我们不需要重新计算结果。

因为在上一步，一些后代改变了，我们需要重新评价他们的适应度。只需要评价那些适应度无效的后代。
```python
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
```
最后，使种群更新为我们计算出来的后代。
```python
        pop[:] = offspring
```
检查进化的性能,我们打印所有个体的适应度的最小,最大,平均值以及他们的标准差。
```python
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
```
最终结果将是有一个个体全为1。

<a name="完整代码"></a>
## 完整代码
```python
# -*- coding: utf-8 -*-


#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.


#    example which maximizes the sum of a list of integers
#    each of which can be 0 or 1

import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
#                      define 'attr_bool' to be an attribute ('gene')
#                      which corresponds to integers sampled uniformly
#                      from the range [0,1] (i.e. 0 or 1 with equal
#                      probability)
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers
#                         define 'individual' to be an individual
#                         consisting of 100 'attr_bool' elements ('genes')
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_bool, 100)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# the goal ('fitness') function to be maximized
def evalOneMax(individual):
    return sum(individual),

#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", evalOneMax)

# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)

#----------

def main():
    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=300)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while max(fits) < 100 and g < 1000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum([x*x for x in fits])
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

if __name__ == "__main__":
    main()

```
