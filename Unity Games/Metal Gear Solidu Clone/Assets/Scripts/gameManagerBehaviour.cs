using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class gameManagerBehaviour : MonoBehaviour {

    public Transform elevatorDoor;
    public Transform player;
    bool isOpening = false;
    float iniTime = 0;

    public void OpenDoor()
    {
        isOpening = true;
        iniTime = Time.time;
    }
    public void EndGame()
    {
        player.gameObject.SetActive(false);
        print("You Win!");
    }
    
    void Update()
    {
        if(isOpening)
        {

            if (Time.time - iniTime > 2f)
            {
                elevatorDoor.gameObject.SetActive(false);
                isOpening = false;
            }
                

        }
    }

}
