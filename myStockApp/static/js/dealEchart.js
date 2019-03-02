
function show_k_line(data,type) {
    var myChart = echarts.init(document.getElementById('K-line-box'));
    //计算MA平均线，N日移动平均线=N日收盘价之和/N  dayCount要计算的天数(5,10,20,30)
    function calculateMA(Count) {
        var result = [];
        for (var i = 0, len = data.values.length; i < len; i++) {
            if (i < Count) {
                result.push('-');
                //alert(result);
                continue;   //结束单次循环，即不输出本次结果
            }
            var sum = 0;
            for (var j = 0; j < Count; j++) {
                //收盘价总和
                sum += data.values[i - j][1];
                //alert(sum);
            }
            result.push(sum / Count);
            // alert(result);
        }
        return result;
    }

    option = {
        title: {    //标题
            text: type,
            left: 0
        },
        tooltip: {  //提示框
            trigger: 'axis',    //触发类型：坐标轴触发
            axisPointer: {  //坐标轴指示器配置项
                type: 'cross'   //指示器类型，十字准星
            }
        },
        legend: {   //图例控件
            data: [type, 'MA5', 'MA10', 'MA20', 'MA30']
        },
        grid: [{     //直角坐标系k
            show: true,
            left: '7%',    //grid组件离容器左侧的距离
            right: '3%',
            height:'60%',
            top:'8%',
            backgroundColor:'#ccc'
        }, {     //直角坐标系vol
            show: true,
            left: '7%',    //grid组件离容器左侧的距离
            right: '3%',
            height:'15%',
            top:'69%',
            backgroundColor:'#ccc'
        }, {     //直角坐标系macd
            show: true,
            left: '7%',    //grid组件离容器左侧的距离
            right: '3%',
            height:'11%',
            top:'85%',
            backgroundColor:'#ccc'
        }
        ],
        xAxis: [{
            type: 'category',   //坐标轴类型，类目轴
            data: data.categoryData,
            minInterval:1,
            boundaryGap: false,    //刻度作为分割线，标签和数据点会在两个刻度上
            axisLine: {onZero: false},
            splitLine: {show: false},   //是否显示坐标轴轴线
            min: 'dataMin', //特殊值，数轴上的最小值作为最小刻度
            max: 'dataMax'  //特殊值，数轴上的最大值作为最大刻度
        },{
      type: 'category',
      gridIndex: 1,
      data: data.categoryData,
      axisLabel: {show: false}
  },{
      type: 'category',
      gridIndex: 2,
      data: data.categoryData,
      axisLabel: {show: false}
  }],
        yAxis: [{
            scale: true,    //坐标刻度不强制包含零刻度
            splitArea: {
                show: true  //显示分割区域
            }
        },{
      gridIndex: 1,
      splitNumber: 3,
      axisLine: {onZero: false},
      axisTick: {show: false},
      splitLine: {show: false},
      axisLabel: {show: true}
  },{
	  gridIndex: 2,
      splitNumber: 4,
      axisLine: {onZero: false},
      axisTick: {show: false},
      splitLine: {show: false},
      axisLabel: {show: true}
  }],
        dataZoom: [     //用于区域缩放
            {
                filterMode: 'filter',    //当前数据窗口外的数据被过滤掉来达到数据窗口缩放的效果  默认值filter
                type: 'inside', //内置型数据区域缩放组件
                xAxisIndex: [0, 0],
                start: 50,      //数据窗口范围的起始百分比
                end: 100        //数据窗口范围的结束百分比
            },
            {
                show: true,
                type: 'slider', //滑动条型数据区域缩放组件
                xAxisIndex: [0, 1],
                y: '90%',
                top: '96%',
                start: 50,
                end: 100,
                
            },{
            show: false,
                xAxisIndex: [0, 2],
                type: 'slider',
                start: 50,
                end: 100
        }
        ],
        series: [   //图表类型
            {
                name: type,
                type: 'candlestick',    //K线图，也可以表示为k
                data: data.values,     //y轴对应的数据
                ////////////////////////图标标注/////////////////////////////
                markPoint: {    //图表标注
                    label: {    //标注的文本
                        normal: {   //默认不显示标注
                            show: true,
                            //position:['20%','30%'],
                            formatter: function (param) {   //标签内容控制器
                                return param != null ? Math.round(param.value) : '';
                            }
                        }
                    },
                    data: [     //标注的数据数组
                        {
                            name: 'XX标点',
                            coord: ['2013/5/31', 2300], //指定数据的坐标位置
                            value: 2300,
                            itemStyle: {    //图形样式
                                normal: {color: 'rgb(41,60,85)'}
                            }
                        },
                        //k线图谱数据显示最大值和最小值以及平均值标志
                        {
                            name: 'highest value',
                            type: 'max',    //最大值
                            valueDim: 'highest'     //在highest维度上的最大值 最高价
                        },
                        {
                            name: 'lowest value',
                            type: 'min',
                            valueDim: 'lowest'  //最低价
                        },
                        {
                            name: 'average value on close',
                            type: 'average',
                            valueDim: 'close'   //收盘价
                        }

                    ],
                    tooltip: {      //提示框
                        formatter: function (param) {
                            return param.name + '<br>' + (param.data.coord || '');
                        }
                    }
                },


                markLine: { //图标标线
                    symbol: ['none', 'none'],   //标线两端的标记类型
                    data: [
                        {
                            name: 'min line on close', //最小值标线
                            type: 'min',
                            valueDim: 'close'
                        },
                        {
                            name: 'max line on close',//最大值标线
                            type: 'max',
                            valueDim: 'close'
                        }
                    ]
                }
            },

            {   //MA5 5天内的收盘价之和/5
                name: 'MA5',
                type: 'line',
                data: calculateMA(5),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: calculateMA(10),
                smooth: true,
                lineStyle: {    //标线的样式
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: calculateMA(20),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA30',
                type: 'line',
                data: calculateMA(30),
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
          name: 'Volumn',
          type: 'bar',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: data.volumes,
          itemStyle: {
	    	  normal: {
		          color: function(params) {
		              var colorList;
		              if (data.values[params.dataIndex][1]>data.values[params.dataIndex][0]) {
		                  colorList = '#ef232a';
		              } else {
		                  colorList = '#314656';
		              }
		              return colorList;
		          },
		      }
	      }
      }
      ,{
          name: 'MACD',
          type: 'bar',
          xAxisIndex: 2,
          yAxisIndex: 2,
          data: data.macd,
          itemStyle: {
	    	  normal: {
		          color: function(params) {
		              var colorList;
		              if (params.data >= 0) {
		                  colorList = '#ef232a';
		              } else {
		                  colorList = '#314656';
		              }
		              return colorList;
		          },
		      }
	      }
      },{
          name: 'DIF',
          type: 'line',
          xAxisIndex: 2,
          yAxisIndex: 2,
          data: data.diff
      },{
          name: 'DEA',
          type: 'line',
          xAxisIndex: 2,
          yAxisIndex: 2,
          data: data.dea
      }
        ]
    };
    // 使用刚指定的配置项和数据显示图表
    myChart.setOption(option);
}


function show_calendar(data){
var dateList = data.dateList

var Data = [];
for (var i = 0; i < dateList.length; i++) {
    Data.push([
        dateList[i],
        1
    ]);
}
option = {
    visualMap: {
                show: false,
                min: 0,
                max: 300,
                calculable: true,
                seriesIndex: [2],
                orient: 'horizontal',
                left: 'center',
                bottom: 0,
                inRange: {
                    color: ['#fff', '#fff']
                }
            },
    calendar: [{
        left: 'center',
        top: 'middle',
        cellSize: [35, 35],
        yearLabel: {show: false},
        orient: 'vertical',
        dayLabel: {
            firstDay: 1,
            nameMap: 'cn'
        },
        range: '2019-03'
    }],
    series: [{
        type: 'scatter',
        coordinateSystem: 'calendar',
        symbolSize: 20,
        label: {
            normal: {
                show: true,
                formatter: function (params) {
                    var d = echarts.number.parseDate(params.value[0]);
                    return d.getDate();
                },
                textStyle: {
                    color: '#000'
                }
            }
        },
        data: Data
    }
]
};
 myChart.setOption(option);
}


function show_stock_mark(data,type){
    var myChart = echarts.init(document.getElementById('lineChart-box'));
option = {
    tooltip: {
        trigger: 'axis',
        position: function (pt) {
            return [pt[0], '10%'];
        }
    },
    title: {
        left: 'left',
        text: type,
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: data.categoryData
    },
    yAxis: {
        type: 'value',
        boundaryGap: [0, '100%'],
        splitLine: {
            show: false
        }
    },
    dataZoom: [
        {
            type: 'inside',
            start: 99.5,
            end: 100
        },
        {
            show: true,
            type: 'slider',
            y: '90%',
            start: 99.5,
            end: 100
        }
    ],
    series: [
        {
            name:'指数点数',
            type:'line',
            smooth:true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                color: "#FF4683"
            },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: "#FF9E44"
                }, {
                    offset: 1,
                    color:"#FF4683"
                }])
            },
            data: data.values
        }
    ]
};
  // 使用刚指定的配置项和数据显示图表
    myChart.setOption(option);
}