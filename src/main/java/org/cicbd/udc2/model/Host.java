package org.cicbd.udc2.model;

import java.util.HashMap;
import java.util.Map;

public class Host {
	private Long id;
	private String hostname;
	private Map<String, Map<String, String>> metrics = new HashMap<>();
	
	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}
	public String getHostname() {
		return hostname;
	}
	public void setHostname(String hostname) {
		this.hostname = hostname;
	}
	public Map<String, Map<String, String>> getMetrics() {
		return metrics;
	}
	public void setMetrics(Map<String, Map<String, String>> metrics) {
		this.metrics = metrics;
	}
	
}
