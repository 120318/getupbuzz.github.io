---
layout: post
title: Go程序性能分析
category: Programming Language
---

在计算机行业里，分析程序性能的工具一般称为Profiling工具，而Profiling在这里主要是分析/剖析的含义。
而Profiling工具能做的很多，比如你想查询哪一段代码占用了大量的CPU，又是哪一段代码分配了大量内存，导致你内存不足等等。

本文会介绍一下Go内置的Profiling工具**pprof**及使用方式。

若想分析一段Go程序的性能情况,需要在代码中引入pprof相关的Package。Golang提供了两个相关的包来帮助用户分析自己的代码，分别是：

* `"runtime/pprof" `
* `"net/http/pprof"`

`"net/http/pprof"`包确切说应该是`"runtime/pprof" `包的封装。`"net/http/pprof"`面向**运行中**的HTTP服务器，所以如果你要分析一个运行中的HTTP服务器的性能，你需要使用`"net/http/pprof"`包，而`“runtime/pprof"`包的作用是对一段运行后的代码Dump出性能分析结果，比如说你想分析一段排序代码，那么你要使用`"runtime/pprof"`包。

对于使用`"net/http/pprof"`包来说，只需要添加一行代码即可：
```go
import _ "net/http/pprof"
```
相对来说，使用`"runtime/pprof"`则麻烦一些，需要
```go
var cpuprofile = flag.String("cpuprofile", "", "write cpu profile to file")

func main() {
    flag.Parse()
    if *cpuprofile != "" {
        f, err := os.Create(*cpuprofile)
        if err != nil {
            log.Fatal(err)
        }
        pprof.StartCPUProfile(f)
        defer pprof.StopCPUProfile()
    }
    ...
```
运行的时候需要
```sh
./exec -cpuprofile=output.prof
```
无论使用那种方式，最终都会得到有关cpu、内存、阻塞、goroutine等信息的prof文件，接下来以[Go Blog](https://blog.golang.org/profiling-go-programs)所举的例子，即[Hundt's benchmark programs](https://github.com/hundt98847/multi-language-bench)中的Golang实现进行阐述。（此示例使用Golang版本较低，如果使用高版本Go环境测试的需要进行手动修改编译）

以**cpu**的prof文件举例，进入go tool pprof 交互界面，输入`top`命令可得。（以flat排序，展示前十个结点）(省略了一些无关信息)

```sh
(pprof) top
Showing nodes accounting for 28s, 56.60% of 49.47s total
Dropped 172 nodes (cum <= 0.25s)
Showing top 10 nodes out of 97
  flat  flat%   sum%        cum   cum%
  8.29s 16.76% 16.76%     17.77s 35.92%  runtime.scanobject
  4.51s  9.12% 25.87%         5s 10.11%  runtime.heapBitsForObject 
  3.55s  7.18% 33.05%     24.27s 49.06%  havlak/havlakloopfinder.FindLoops
  2.09s  4.22% 37.28%      8.06s 16.29%  runtime.mallocgc 
  2.05s  4.14% 41.42%      2.44s  4.93%  runtime.mapaccess1_fast64 
  1.89s  3.82% 45.24%      5.72s 11.56%  runtime.mapassign_fast64 
  1.74s  3.52% 48.76%      1.74s  3.52%  runtime.memmove 
  1.52s  3.07% 51.83%      1.66s  3.36%  runtime.heapBitsSetType 
  1.22s  2.47% 54.30%      1.58s  3.19%  runtime.mapiternext 
  1.14s  2.30% 56.60%      1.14s  2.30%  runtime.memclrNoHeapPointers 
```
释义：
1. 第一列，第二列的`flat`代表着对应函数所占cpu时间和百分比，单纯的表示此函数自己执行的时间，不包括在此函数中调用其他函数的等待时间。
2. 第四列，第五列的`cum`代表着累积分调用所占cpu时间和百分比，代表着采样中取到了此函数而且包括此函数中调用其他子函数。所以可以看出`cum`可能会比`flat`高很多。
3. 第三列`sum`代表着此列表中前几项的直接调用`flat`所占百分比和，是个累计值。
4. 此列表展示了172个结点采样，摒弃了`cum < 0.25s`的结点，展示了占用cpu消耗的前10项，共占总消耗百分之56.60%。

通过`flat`和`cum`我们可以很容易的看出哪些func/语句占用了大量的CPU。  
同时，在pprof交互界面中还有一些其他命令，如`web`等可以把结果输出成图结构，`list`等可以展示某个函数的详细细节代码，命令比较简单，`help`里很容易查到使用方法，不详细介绍。

---

####  参考

[Go Blog](https://blog.golang.org/profiling-go-programs)

[Go 命令教程](https://github.com/hyper0x/go_command_tutorial/blob/master/0.12.md)
