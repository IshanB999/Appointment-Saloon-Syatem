var ICChartsWidget1 = {
    init: function() {
        ! function() {
            var e = document.getElementById("ic_charts_widget_1");
            if (e) {
                var a = parseInt(KTUtil.css(e, "height")),
                    t = KTUtil.getCssVariableValue("--bs-gray-500"),
                    l = KTUtil.getCssVariableValue("--bs-border-dashed-color"),
                    o = KTUtil.getCssVariableValue("--cu-success"),
                    r = KTUtil.getCssVariableValue("--cu-success"),
                    i = new ApexCharts(e, {
                        series: [{
                            name: "Sales",
                            data: [18, 18, 20, 20, 18, 18, 22, 22, 20, 20, 18, 18, 20, 20, 18, 18, 20, 20, 22]
                        }],
                        chart: {
                            fontFamily: "inherit",
                            type: "area",
                            height: a,
                            toolbar: {
                                show: !1
                            }
                        },
                        plotOptions: {},
                        legend: {
                            show: !1
                        },
                        dataLabels: {
                            enabled: !1
                        },
                        fill: {
                            type: "gradient",
                            gradient: {
                                shadeIntensity: 1,
                                opacityFrom: .4,
                                opacityTo: 0,
                                stops: [0, 80, 100]
                            }
                        },
                        stroke: {
                            curve: "smooth",
                            show: !0,
                            width: 3,
                            colors: [o]
                        },
                        xaxis: {
                            categories: ["", "Apr 02", "Apr 03", "Apr 04", "Apr 05", "Apr 06", "Apr 07", "Apr 08", "Apr 09", "Apr 10", "Apr 11", "Apr 12", "Apr 13", "Apr 14", "Apr 15", "Apr 16", "Apr 17", "Apr 18", ""],
                            axisBorder: {
                                show: !1
                            },
                            axisTicks: {
                                show: !1
                            },
                            tickAmount: 6,
                            labels: {
                                rotate: 0,
                                rotateAlways: !0,
                                style: {
                                    colors: t,
                                    fontSize: "12px"
                                }
                            },
                            crosshairs: {
                                position: "front",
                                stroke: {
                                    color: o,
                                    width: 1,
                                    dashArray: 3
                                }
                            },
                            tooltip: {
                                enabled: !0,
                                formatter: void 0,
                                offsetY: 0,
                                style: {
                                    fontSize: "12px"
                                }
                            }
                        },
                        yaxis: {
                            tickAmount: 4,
                            max: 24,
                            min: 10,
                            labels: {
                                style: {
                                    colors: t,
                                    fontSize: "12px"
                                },
                                formatter: function(e) {
                                    return "$" + e + "K"
                                }
                            }
                        },
                        states: {
                            normal: {
                                filter: {
                                    type: "none",
                                    value: 0
                                }
                            },
                            hover: {
                                filter: {
                                    type: "none",
                                    value: 0
                                }
                            },
                            active: {
                                allowMultipleDataPointsSelection: !1,
                                filter: {
                                    type: "none",
                                    value: 0
                                }
                            }
                        },
                        tooltip: {
                            style: {
                                fontSize: "12px"
                            },
                            y: {
                                formatter: function(e) {
                                    return "$" + e + "K"
                                }
                            }
                        },
                        colors: [r],
                        grid: {
                            borderColor: l,
                            strokeDashArray: 4,
                            yaxis: {
                                lines: {
                                    show: !0
                                }
                            }
                        },
                        markers: {
                            strokeColor: o,
                            strokeWidth: 3
                        }
                    });
                setTimeout((function() {
                    i.render()
                }), 200)
            }
        }()
    }
};
"undefined" != typeof module && (module.exports = ICChartsWidget1), KTUtil.onDOMContentLoaded((function() {
    ICChartsWidget1.init()
}));

