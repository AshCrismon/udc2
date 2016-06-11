package org.cicbd.udc2.vo;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class HostMetricVo {

	private String hostname;
	private Map<String, List<MetricVo>> metrics = new HashMap<>();
	public String getHostname() {
		return hostname;
	}
	public void setHostname(String hostname) {
		this.hostname = hostname;
	}
	public Map<String, List<MetricVo>> getMetrics() {
		return metrics;
	}
	public void setMetrics(Map<String, List<MetricVo>> metrics) {
		this.metrics = metrics;
	}
}
