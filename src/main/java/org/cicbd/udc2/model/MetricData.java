package org.cicbd.udc2.model;

public class MetricData {

	private Long clock;
	private String value;
	
	public Long getClock() {
		return clock;
	}
	public void setClock(Long clock) {
		this.clock = clock;
	}
	public String getValue() {
		return value;
	}
	public void setValue(String value) {
		this.value = value;
	}
	@Override
	public String toString() {
		return "MetricData [clock=" + clock + ", value=" + value + "]";
	}

}
