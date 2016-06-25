package org.cicbd.udc2.model;

import org.bson.types.ObjectId;

public class MetricInfo {

	private ObjectId id;
	private String mid;
	private String TITLE;
	private String DESC;
	private String GROUP;
	private String tn;
	private String tmax;
	private String dmax;
	private String units;
	private String source;
	public ObjectId getId() {
		return id;
	}
	public void setId(ObjectId id) {
		this.id = id;
	}
	public String getMid() {
		return mid;
	}
	public void setMid(String mid) {
		this.mid = mid;
	}
	public String getTITLE() {
		return TITLE;
	}
	public void setTITLE(String tITLE) {
		TITLE = tITLE;
	}
	public String getDESC() {
		return DESC;
	}
	public void setDESC(String dESC) {
		DESC = dESC;
	}
	public String getGROUP() {
		return GROUP;
	}
	public void setGROUP(String gROUP) {
		GROUP = gROUP;
	}
	public String getTn() {
		return tn;
	}
	public void setTn(String tn) {
		this.tn = tn;
	}
	public String getTmax() {
		return tmax;
	}
	public void setTmax(String tmax) {
		this.tmax = tmax;
	}
	public String getDmax() {
		return dmax;
	}
	public void setDmax(String dmax) {
		this.dmax = dmax;
	}
	public String getUnits() {
		return units;
	}
	public void setUnits(String units) {
		this.units = units;
	}
	public String getSource() {
		return source;
	}
	public void setSource(String source) {
		this.source = source;
	}
	@Override
	public String toString() {
		return "MetricInfo [id=" + id + ", mid=" + mid + ", TITLE=" + TITLE
				+ ", DESC=" + DESC + ", GROUP=" + GROUP + ", tn=" + tn
				+ ", tmax=" + tmax + ", dmax=" + dmax + ", units=" + units
				+ ", source=" + source + "]";
	}

}
