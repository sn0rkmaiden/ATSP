from collections import defaultdict


class MeasurementLog:

    def __init__(self):
        self.factory = lambda: {
            'temperatures': [],
            'costs': []
        }
        self.timestamps = defaultdict(self.factory)
        self.best = {
            'cost': [],
            'timestamp': [],
            'path': []
        }

    def add_best(self, timestamp, cost, path):
        self.best['cost'].append(cost)
        self.best['timestamp'].append(timestamp)
        self.best['path'].append(path)

    def add(self, timestamp, temperature, cost):
        self.timestamps[timestamp]['temperatures'].append(temperature)
        self.timestamps[timestamp]['costs'].append(cost)

    def generate_report(self):
        report = defaultdict(self.factory)
        for timestamp, stat in self.timestamps.items():
            report[timestamp]['temperatures'] = sum(stat['temperatures'])/len(stat['temperatures'])
            report[timestamp]['costs'] = sum(stat['costs']) / len(stat['costs'])
        return report

    def time_summary(self):
        header = 'Timestamp;Cost;Temperature'
        rows = [header]
        report = self.generate_report()
        for timestamp, stat in report.items():
            rows.append('{};{};{}'.format(round(timestamp), stat['costs'], stat['temperatures']))
        return '\n'.join(rows)

    def best_summary(self):
        header = 'Timestamp;Cost;Path'
        rows = [header]
        for i, _ in enumerate(self.best['cost']):
            rows.append('{};{};{}'.format(round(self.best['timestamp'][i]),
                                          self.best['cost'][i],
                                          self.best['path'][i]))
        return '\n'.join(rows)
