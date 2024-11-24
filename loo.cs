class PanZoom
{
  /* offset if viewport to origin */
  private int offsetX;
  private int offsetY;

  private bool mouseButtonPressed;
  private int mouseStartX;
  private int mouseStartY;

  private float scale = 1.0f;

  public PanZoom(int x = 0, int y = 0)
  {
    this.offsetX = x;
    this.offsetY = y;
  }

  public void ConvertGlobalToScreen(float gx, float gy, out float sx, out float sy)
  {
    /* screen coord = (global coord - offset) * scale */
    sx = (gx - this.offsetX) * this.scale;
    sy = (gy - this.offsetY) * this.scale;
  }

  public void ConvertScreenToGlobal(float sx, float sy, out float gx, out float gy)
  {
    /* global coord = (screen coord / scale) - offset */
    gx = (sx / this.scale) + this.offsetX;
    gy = (sy / this.scale) + this.offsetY;
  }

  public void MouseDown(int x, int y)
  {
    /* mouse button pressed down */
    this.mouseButtonPressed = true;
    /* store initial mouse event coords in panel */
    this.mouseStartX = x;
    this.mouseStartY = y;
  }

  public void MouseUp(int x, int y)
  {
    this.mouseButtonPressed = false;
  }

  public void MouseMove(int x, int y)
  {
    if (this.mouseButtonPressed)
    {
      /* if mouse is moved right, deltaX is positive */
      int deltaX = (int)((x - this.mouseStartX) / this.scale);
      /* if mouse is moved down, deltaY is positive */
      int deltaY = (int)((y - this.mouseStartY) / this.scale);

      /* if deltaX is positive, then the viewport seems to move right,
        meaning that the objects shall move left, therefore the x offset shall be increased */
      this.offsetX -= deltaX;
      /* if deltaY is positive, then the viewport seems to move down,
        meaning that the objects shall move up, therefore the y offset shall be increased */
      this.offsetY -= deltaY;

      /* clip to the world coordinates */
      this.offsetX = Math.Max(0, this.offsetX);
      this.offsetY = Math.Max(0, this.offsetY);
      this.offsetX = Math.Min(World.WorldWidth - (int)(World.ViewPortWidth / this.scale), this.offsetX);
      this.offsetY = Math.Min(World.WorldHeight - (int)(World.ViewPortHeight / this.scale), this.offsetY);

      /* start new micro movement */
      this.mouseStartX = x;
      this.mouseStartY = y;
    }
  }

  public void onMouseWheel(int x, int y, int delta)
  {
    /* get the screen coordinate of cursor in global space _before_ the scale factor is updated */
    ConvertScreenToGlobal(x, y, out float gxBefore, out float gyBefore);

    /* update the scale factor based on the mouse wheel movement
      delta > 0 if mouse wheel up, we want to treat this as zoom in */
    if (delta < 0)
    {
      scale *= 0.98f;
    }
    /* delta < 0 if mouse wheel down, we want to treat this as zoom out, so increate scale to draw things bigger */
    else
    {
      scale *= 1.02f;
    }

    /* get new screen position of cursor with applied new zoom factor in global space */
    ConvertScreenToGlobal(x, y, out float gxAfter, out float gyAfter);

    /* correct global panning offset depending on changed cursor pos caused by zoom */
    this.offsetX += (int)(gxBefore - gxAfter);
    this.offsetY += (int)(gyBefore - gyAfter);

    /* clip to the world coordinates */
    this.offsetX = Math.Max(0, this.offsetX);
    this.offsetY = Math.Max(0, this.offsetY);
    this.offsetX = Math.Min(World.WorldWidth - World.ViewPortWidth, this.offsetX);
    this.offsetY = Math.Min(World.WorldHeight - World.ViewPortHeight, this.offsetY);

  }

  public int XOffset { get { return offsetX; } }
  public int YOffset { get { return offsetY; } }

  public float Scale { get { return scale; } }
}