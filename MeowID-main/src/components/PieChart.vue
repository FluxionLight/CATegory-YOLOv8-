<template>
    <div class="p-1">
        <Pie :key="chartKey" :data="chartData" :options="options" />
    </div>
</template>

<script lang="ts">
import { defineComponent, reactive, toRefs, watch, ref } from 'vue'
import {Chart as ChartJS, ArcElement, Tooltip, Legend, type ChartOptions} from 'chart.js'
import { Pie } from 'vue-chartjs'
import ChartDataLabels from 'chartjs-plugin-datalabels'  // 引入 datalabels 插件

// 注册 chart.js 的元素和插件
ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels)

export default defineComponent({
    name: 'App',
    components: {
        Pie
    },
    props: {
        // 父组件传入 labels 和 data
        labels: {
            type: Array as () => number[],
            required: true
        },
        data: {
            type: Array as () => number[],
            required: true
        }
    },
    setup(props) {
        const chartKey = ref(0) // 用于强制重新渲染图表

        // 使用 reactive 来定义响应式对象
        const chartConfig = reactive({
            chartData: {
                labels: props.labels,
                datasets: [
                    {
                        backgroundColor: [
                            '#6a1b9a', '#f44336', '#ff9800', '#4caf50', '#2196f3',
                            '#9c27b0', '#03a9f4', '#8bc34a', '#ffeb3b', '#00bcd4'
                        ],
                        data: props.data
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top' as const, // 这里使用 'top' 并通过 `as const` 保证其类型正确
                    },
                    tooltip: {
                        callbacks: {
                            label: (context: any) => {
                                return (context.raw).toFixed(2) + '%'; // 显示百分比
                            }
                        }
                    },
                    datalabels: {
                        color: '#fff', // 设置标签字体颜色
                        formatter: (value: number) => {
                            return value.toFixed(2) + '%'; // 显示百分比
                        },
                        font: {
                            weight: 'bold',
                            size: 14
                        },
                        align: 'center',  // 标签水平居中
                        anchor: 'center'  // 标签垂直居中
                    }
                }
            } as ChartOptions<'pie'>, // 强制类型为 ChartOptions
        })

        // 使用 watch 来监听 props 的变化并更新 chartData
        watch(
            () => [props.labels, props.data],
            ([newLabels, newData]) => {
                chartConfig.chartData.labels = newLabels
                chartConfig.chartData.datasets[0].data = newData

                // 更新 chartKey 强制重新渲染
                chartKey.value += 1
            },
            { immediate: true } // 立即执行一次，确保初始化时数据被设置
        )

        // 返回响应式数据
        return {
            ...toRefs(chartConfig),
            chartKey
        }
    }
})
</script>