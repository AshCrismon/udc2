package org.cicbd.udc2.repository;

import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.List;

import org.bson.types.ObjectId;
import org.cicbd.udc2.exception.CollectionNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

import com.mongodb.DBCollection;

@Repository
public abstract class CommonRepository<Entity> implements BaseRepository<Entity> {
	
	@Autowired
	protected MongoTemplate mongo;
	protected Class<Entity> entityClass;
	
	@SuppressWarnings("unchecked")
	public CommonRepository(){
		Type type = getClass().getGenericSuperclass();
		if (type instanceof ParameterizedType) {
			Type[] types = ((ParameterizedType) type).getActualTypeArguments();
			entityClass = (Class<Entity>) types[0];
		}
	}
	
	@Override
	public List<Entity> findAll(String collectionName){
		return mongo.findAll(entityClass, collectionName);
	}
	
	@Override
	public List<Entity> find(Query query, String collectionName){
		return mongo.find(query, entityClass, collectionName);
	}
	
	@Override
	public Entity findOne(Query query, String collectionName){
		return mongo.findOne(query, entityClass, collectionName);
	}
	
	@Override
	public Entity findById(ObjectId id, String collectionName){
		return mongo.findById(id, entityClass, collectionName);
	}
	
	@Override
	public Entity findById(String id, String collectionName){
		return findById(new ObjectId(id), collectionName);
	}
	
	@Override
	public List<Entity> findAllAndRemove(Query query, String collectionName){
		return mongo.findAllAndRemove(query, entityClass, collectionName);
	}
	
	@Override
	public Entity findAndRemove(Query query, String collectionName){
		return mongo.findAndRemove(query, entityClass, collectionName);
	}
	
	@Override
	public DBCollection createCollection(String collectionName){
		return mongo.createCollection(collectionName);
	}
	
	@Override
	public void dropCollection(String collectionName){
		mongo.dropCollection(collectionName);
	}
	
	protected void validateCollection(String collectionName){
		if(!mongo.collectionExists(collectionName)){
			throw new CollectionNotFoundException(collectionName);
		}
	}
}
