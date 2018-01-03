using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cameraBehaviour : MonoBehaviour {

    public Transform player;
    Vector3 cameraPosition;

	// Use this for initialization
	void Start ()
    {
        cameraPosition = new Vector3(0, 30, -10);

    }
	
	// Update is called once per frame
	void Update ()
    {
        if(player != null)
            transform.position = player.position + cameraPosition;
	}
}
