package org.cicbd.udc2.exception;

public class CollectionNotFoundException extends RuntimeException{

	private static final long serialVersionUID = 1L;
	
	public CollectionNotFoundException(String collectionName){
		super("collection [" + collectionName + "] not found");
	}

}
