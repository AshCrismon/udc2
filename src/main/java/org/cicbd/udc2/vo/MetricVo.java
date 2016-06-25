package org.cicbd.udc2.vo;

public class MetricVo {

	private Long clock;
	private Double value;
	
	
	public Long getClock() {
		return clock;
	}
	public void setClock(Long clock) {
		this.clock = clock;
	}
	public Double getValue() {
		return value;
	}
	public void setValue(Double value) {
		this.value = value;
	}
	@Override
	public String toString() {
		return "MetricVo [clock=" + clock + ", value=" + value + "]";
	}
	
}
