package org.cicbd.udc2.vo;

public class MetricVo {

	private Long timestamp;
	private Double value;
	
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
		return "MetricVo [timestamp=" + timestamp + ", value=" + value + "]";
	}
	
}
