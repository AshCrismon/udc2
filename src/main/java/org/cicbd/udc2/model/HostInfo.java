package org.cicbd.udc2.model;

import org.bson.types.ObjectId;

public class HostInfo {
	private ObjectId id;
	private String hid;
	private String ip;
	private String cluster;
	private String gmond_started;
	private String name;
	private String tags;
	private String tmax;
	private String tn;
	private String location;
	private String dmax;
	public ObjectId getId() {
		return id;
	}
	public void setId(ObjectId id) {
		this.id = id;
	}
	public String getHid() {
		return hid;
	}
	public void setHid(String hid) {
		this.hid = hid;
	}
	public String getIp() {
		return ip;
	}
	public void setIp(String ip) {
		this.ip = ip;
	}
	public String getCluster() {
		return cluster;
	}
	public void setCluster(String cluster) {
		this.cluster = cluster;
	}
	public String getGmond_started() {
		return gmond_started;
	}
	public void setGmond_started(String gmond_started) {
		this.gmond_started = gmond_started;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getTags() {
		return tags;
	}
	public void setTags(String tags) {
		this.tags = tags;
	}
	public String getTmax() {
		return tmax;
	}
	public void setTmax(String tmax) {
		this.tmax = tmax;
	}
	public String getTn() {
		return tn;
	}
	public void setTn(String tn) {
		this.tn = tn;
	}
	public String getLocation() {
		return location;
	}
	public void setLocation(String location) {
		this.location = location;
	}
	public String getDmax() {
		return dmax;
	}
	public void setDmax(String dmax) {
		this.dmax = dmax;
	}
	@Override
	public String toString() {
		return "HostInfo [id=" + id + ", hid=" + hid + ", ip=" + ip
				+ ", cluster=" + cluster + ", gmond_started=" + gmond_started
				+ ", name=" + name + ", tags=" + tags + ", tmax=" + tmax
				+ ", tn=" + tn + ", location=" + location + ", dmax=" + dmax
				+ "]";
	}
}
