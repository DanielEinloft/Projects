using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class GameManager : MonoBehaviour {

    public Rigidbody doorRb;
    public GameObject Panel;

    private bool endGame;
	
    
    // Use this for initialization
	void Start ()
    {
        endGame = false;
	}
	
    public void UnlockDoor()
    {
        doorRb.gameObject.SetActive(false);
    }

    public void GameWon()
    {
        if(!endGame)
        {
            Debug.Log("OH YAS");
            Panel.SetActive(true);
            endGame = true;
        }
        
    }


}
