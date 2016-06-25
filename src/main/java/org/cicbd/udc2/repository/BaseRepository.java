package org.cicbd.udc2.repository;

import java.util.List;

import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.query.Query;

import com.mongodb.DBCollection;

public interface BaseRepository<Entity> {
	
	List<Entity> findAll(String collectionName);
	
	List<Entity> find(Query query, String collectionName);
	
	Entity findById(ObjectId id, String collectionName);
	
	Entity findById(String id, String collectionName);
	
	List<Entity> findAllAndRemove(Query query, String collectionName);
	
	Entity findAndRemove(Query query, String collectionName);
	
	DBCollection createCollection(String collectionName);
	
	void dropCollection(String collectionName);

	Entity findOne(Query query, String collectionName);
	
}
