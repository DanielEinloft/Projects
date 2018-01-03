using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EndGame : MonoBehaviour
{
    public GameObject gameManager;
    private void OnTriggerEnter(Collider other)
    {
        gameManager.GetComponent<gameManagerBehaviour>().EndGame();

    }

}
