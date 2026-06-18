using Microsoft.AspNetCore.Mvc;
using TenderGuard.Api.Models;
using TenderGuard.Api.Services;

namespace TenderGuard.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ReviewsController : ControllerBase
{
    private readonly ReviewService _reviewService;

    public ReviewsController(ReviewService reviewService)
    {
        _reviewService = reviewService;
    }

    [HttpPost("start")]
    public async Task<ActionResult<ReviewCase>> StartReview(StartReviewRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.ContractText))
        {
            return BadRequest("Contract text is required.");
        }

        var review = await _reviewService.StartReviewAsync(request);
        return Ok(review);
    }

    [HttpGet]
    public ActionResult<List<ReviewCase>> GetAllReviews()
    {
        return Ok(_reviewService.GetAllReviews());
    }

    [HttpGet("{id}")]
    public ActionResult<ReviewCase> GetReview(Guid id)
    {
        var review = _reviewService.GetReview(id);

        if (review == null)
        {
            return NotFound();
        }

        return Ok(review);
    }

    [HttpPost("{id}/human-decision")]
    public ActionResult<ReviewCase> AddHumanDecision(Guid id, HumanDecisionRequest request)
    {
        var review = _reviewService.AddHumanDecision(id, request);

        if (review == null)
        {
            return NotFound();
        }

        return Ok(review);
    }
}