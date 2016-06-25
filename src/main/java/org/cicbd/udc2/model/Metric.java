package org.cicbd.udc2.model;

import org.bson.types.ObjectId;

public class Metric extends MetricData{

	private ObjectId id;
	private String metric;
	
	public ObjectId getId() {
		return id;
	}
	public void setId(ObjectId id) {
		this.id = id;
	}
	public String getMetric() {
		return metric;
	}
	public void setMetric(String metric) {
		this.metric = metric;
	}
}
