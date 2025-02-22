class Event {
    constructor(name, date, location = '', description = '') {
        if (!name || !date) {
            throw new Error('名称和时间是必填项');
        }
        this.name = name;
        this.date = new Date(date); // 日期格式：YYYY-MM-DD HH:mm
        this.location = location;
        this.description = description;
    }

    // 可以添加其他方法，例如格式化日期、获取事件详情等
}
class EventManager {
    constructor() {
        this.events = [];
    }

    addEvent(event) {
        this.events.push(event);
    }

    deleteEvent(eventName) {
        this.events = this.events.filter(event => event.name !== eventName);
    }

    // 按月份统计事件发生频率
    getEventFrequencyByMonth() {
        const frequency = {};
        this.events.forEach(event => {
            const month = event.date.toLocaleString('default', { month: 'long' });
            if (!frequency[month]) frequency[month] = 0;
            frequency[month]++;
        });
        return frequency;
    }
}

class ChartGenerator {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.chart = null;
    }

    generateBarChart(data) {
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(this.canvas, {
            type: 'bar',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    label: '事件发生频率',
                    data: Object.values(data),
                    backgroundColor: 'rgba(0, 123, 255, 0.5)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}
