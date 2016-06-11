package org.cicbd.udc2.model;

import org.bson.types.ObjectId;

public class Metric {

	private ObjectId id;
	private String metric;
	private Long timestamp;
	private Double value;
	
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
	public Long getTimestamp() {
		return timestamp;
	}
	public void setTimestamp(Long timestamp) {
		this.timestamp = timestamp;
	}
	public Double getValue() {
		return value;
	}
	public void setValue(Double value) {
		this.value = value;
	}
	@Override
	public String toString() {
		return "Metric [id=" + id + ", metric=" + metric + ", timestamp=" + timestamp
				+ ", value=" + value + "]";
	}
}
